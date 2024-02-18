from app import db, login, config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from .repository import natura_impact_assessment, check_intersection
from geoalchemy2 import Geometry
from shapely.geometry import Point
from sqlalchemy import func, create_engine, MetaData, Table, Column
from sqlalchemy.orm import sessionmaker
import pyproj
from shapely.ops import transform
import geopandas as gpd

engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
metadata_obj = MetaData(schema="data")
Session = sessionmaker(bind=engine)
session = Session()

birds_table = Table("Uredba_NN8019_3_Identifikacijski", 
                        metadata_obj,
                        autoload_with = engine)

natura_habitats = Table("povs", 
                        metadata_obj,
                        Column("geom", Geometry('POLYGON')),
                        autoload_with = engine)

natura_birds = Table("pop", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

def check_povs(data):
    site_code = session.query(natura_habitats.c.sitecode).filter(natura_habitats.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return site_code

def check_pop(data):
    site_code = session.query(natura_birds.c.sitecode).filter(natura_birds.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return site_code[0]

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    message = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(140))
    description = db.Column(db.String(440))
    project_type = db.Column(db.String(140))
    # file = db.Column(db.FileField)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    impact = db.Column(db.String(20000))

    def __init__(self, project_title, description, project_type, lat, lon, user_id):
        self.project_title = project_title
        self.description = description
        self.project_type = project_type
        self.lat = lat
        self.lon = lon
        self.create_point(self.lat, self.lon)

        self.user_id = user_id
        self.assess_impact()
        self.query_birds()
        super().__init__()

    def assess_impact(self):
        self.impact = natura_impact_assessment(self.lat, self.lon, self.project_title, self.project_type)
        return self.impact
    
    def query_birds(self):
        point = self.create_point(self.lat, self.lon)
        site_code = check_pop(point)
        self.birds = session.query(birds_table.c.latin).filter_by(code=site_code[0]).all()
        birds_list = []

        for bird in self.birds:
            bird = bird[0]
            birds_list.append(bird)
        
        return birds_list
    
    def query_birds_table(self):
        point = self.create_point(self.lat, self.lon)
        site_code = check_pop(point)
        self.birds = session.query(birds_table.c.latin, birds_table.c.croatian, birds_table.c.Status_G, birds_table.c.Status_P, birds_table.c.Status_Z).filter_by(code=site_code[0]).all()
        
        return self.birds
    
    def query_povs(self):
        site_code = check_povs(self.point)
    
    def create_point(self, lat, lon):
        # Create a Point object with the given latitude and longitude
        point = Point(lon, lat)

        # Define the target CRS (EPSG:4326)
        target_crs = pyproj.CRS.from_epsg(4326)

        # Define the source CRS (EPSG:4326)
        source_crs = pyproj.CRS.from_epsg(4326)

        # Create a transformer to convert coordinates to the target CRS
        transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

        # Transform the Point object to the target CRS
        transformed_point = transform(transformer.transform, point)

        return point

    def get_geodataframe_for_point(self):
        # Define the query to retrieve data within 5 kilometers of the given point
        query = f"""
            SELECT ST_GeometryN(geom, generate_series(1, ST_NumGeometries(geom))) AS geom_polygon
            FROM data.pop
            WHERE ST_DWithin(
                geom,
                ST_Transform(ST_SetSRID(ST_MakePoint(15.73, 45.61), 4326),3765),
                5000
            )
            LIMIT 5;
        """

        # Use geopandas to read the data from the database into a GeoDataFrame
        gdf = gpd.read_postgis(query, session.bind, geom_col='geom_polygon', crs = 3765)

        return gdf

@login.user_loader
def load_user(id):
    return User.query.get(int(id))