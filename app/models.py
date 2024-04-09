from app import db, login, config, text_templates
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from .tools.report_creation import natura_impact_assessment, natura_description
from geoalchemy2 import Geometry
from sqlalchemy import func, create_engine, MetaData, Table, Column
from sqlalchemy.orm import sessionmaker
import multiprocessing
from datetime import date

from .text_generation import climate_analysis_of_probability
from .tools.geoanalysis import create_point


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

cro_administrative_opcine_gradovi_3765 = Table("cro_administrative_opcine_gradovi_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_bentos_3765 = Table("cro_bio_bentos_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_habitats_2004_3765 = Table("cro_bio_habitats_2004_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_habitats_2016_3765 = Table("cro_bio_habitats_2016_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_mab_3765 = Table("cro_bio_mab_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_zpp_points_3765 = Table("cro_bio_zpp_points_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_bio_zpp_polygons_3765 = Table("cro_bio_zpp_polygons_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_forest_private_gj_3765 = Table("cro_forest_private_gj_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

cro_forest_private_unit_3765 = Table("cro_forest_private_unit_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

esri_water_bodies_3765 = Table("esri_water_bodies_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

osm_rivers_lines_3765 = Table("osm_rivers_lines_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)

osm_rivers_polygons_3765 = Table("osm_rivers_polygons_3765", 
                    metadata_obj,
                    Column("geom", Geometry('POLYGON')),
                    autoload_with = engine)


def get_natura_povs(data):
    site_code = session.query(natura_habitats.c.sitecode).filter(natura_habitats.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return site_code

def get_natura_pop(data):
    site_code = session.query(natura_birds.c.sitecode, natura_birds.c.sitename).filter(natura_birds.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return site_code

def get_administrative_cro(data):
    administrative = session.query(cro_administrative_opcine_gradovi_3765.c.shapename).filter(cro_administrative_opcine_gradovi_3765.c.geom.contains(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return administrative

def get_habitats_2004(data):
    habitats = session.query(cro_bio_habitats_2004_3765.c.nks_kod, 
                             cro_bio_habitats_2004_3765.c.nks_ime).filter(cro_bio_habitats_2004_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return habitats

def get_habitats_2016(data):
    habitats = session.query(cro_bio_habitats_2016_3765.c.nks1, 
                             cro_bio_habitats_2016_3765.c.nks1_naziv).filter(cro_bio_habitats_2016_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return habitats

def get_mab_cro(data):
    mab = session.query(cro_bio_mab_3765.c.naziv, cro_bio_mab_3765.c.zona).filter(cro_bio_mab_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return mab


def get_zpp_points(data):
    result = session.query(cro_bio_zpp_points_3765.c.kategorija,
                           cro_bio_zpp_points_3765.c.naziv_akt,
                           func.ST_Distance(cro_bio_zpp_points_3765.c.geom,
                                            func.ST_Transform(data.wkt, 
                                                              'EPSG: 4326', 
                                                              3765)).label('distance')).filter(cro_bio_zpp_points_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result


def get_zpp_polygons(data):
    result = session.query(cro_bio_zpp_polygons_3765.c.kategori_1, 
                           cro_bio_zpp_polygons_3765.c.naziv_akt, 
                           func.ST_Distance(
                               cro_bio_zpp_polygons_3765.c.geom, 
                               func.ST_Transform(
        data.wkt, 'EPSG: 4326', 3765)).label('distance')).filter(cro_bio_zpp_polygons_3765.c.geom.intersects(
            func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result

def get_forest_private_gj(data):
    result = session.query(cro_forest_private_gj_3765.c.ngj, cro_forest_private_gj_3765.c.gj, func.ST_Distance(cro_forest_private_gj_3765.c.geom, func.ST_Transform(data.wkt,
    'EPSG: 4326', 3765)).label('distance')).filter(cro_forest_private_gj_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result

def get_forest_private_unit(data):
    result = session.query(cro_forest_private_unit_3765.c.odjel, cro_forest_private_unit_3765.c.odsjek, cro_forest_private_unit_3765.c.povrsina, func.ST_Distance(cro_forest_private_unit_3765.c.geom, func.ST_Transform(data.wkt,
    'EPSG: 4326', 3765)).label('distance')).filter(cro_forest_private_unit_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result

def get_esri_water_bodies(data):
    result = session.query(esri_water_bodies_3765.c.name1, esri_water_bodies_3765.c.type, func.ST_Distance(esri_water_bodies_3765.c.geom, func.ST_Transform(data.wkt,
    'EPSG: 4326', 3765)).label('distance')).filter(esri_water_bodies_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result

def get_osm_rivers_lines(data):
    result = session.query(osm_rivers_lines_3765.c.name, osm_rivers_lines_3765.c.waterway, func.ST_Distance(osm_rivers_lines_3765.c.geom, func.ST_Transform(data.wkt,
    'EPSG: 4326', 3765)).label('distance')).filter(osm_rivers_lines_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result

def get_osm_rivers_polygons(data):
    result = session.query(osm_rivers_polygons_3765.c.name, func.ST_Distance(osm_rivers_polygons_3765.c.geom, func.ST_Transform(data.wkt,
    'EPSG: 4326', 3765)).label('distance')).filter(osm_rivers_polygons_3765.c.geom.intersects(func.ST_transform(data.wkt, 'EPSG: 4326', 3765))).all()
    return result


def query_all(data):
    functions = [
        get_natura_povs,
        get_natura_pop,
        get_administrative_cro,
        get_habitats_2004,
        get_habitats_2016,
        get_mab_cro,
        get_zpp_points,
        get_zpp_polygons,
        get_forest_private_gj,
        get_forest_private_unit,
        get_esri_water_bodies,
        get_osm_rivers_lines,
        get_osm_rivers_polygons
    ]

    results = {}

    for func in functions:
        result = func(data)
        results[func.__name__] = result

    return results


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
    # report_type = db.Column(db.String(140))
    # experts = db.Column(db.String(140))
    # file = db.Column(db.FileField)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    date_created = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    impact = db.Column(db.String(20000))

    def __init__(self, project_title, description, project_type, lat, lon, user_id):
        self.project_title = project_title
        self.description = description
        self.project_type = project_type
        self.lat = lat
        self.lon = lon
        self.point = create_point(self.lat, self.lon)
        self.chapters = None
        # self.chapters = db.relationship('Chapter', backref='author', lazy='dynamic')

        self.user_id = user_id
        # self.query_birds_table()
        # self.get_description()
        self.impact = natura_impact_assessment(lat, lon, project_title, project_type)
        super().__init__()

    def assess_impact(self):
        impact = natura_impact_assessment(self.lat, self.lon, self.project_title, self.project_type)
        return impact
    

class Chapter():
    def __init__(self, project_id, heading, description, impact, table, image, source) -> None:
        # TODO: One-to-many relationship between project and chapters
        self.project_id = project_id
        self.heading = heading
        self.description = description
        self.impact = impact
        self.table = table
        self.image = image
        self.source = source
        self.query = None
        pass


class NaturaChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:
        # super().__init__(project_id)

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type

        self.point = create_point(lat, lon)
        # natura specific
        self.heading = text_templates["natura2000_heading"]
        # natura pop
        natura_pop = get_natura_pop(self.point)
        if natura_pop:
            self.site_code = natura_pop[0][0]
            self.site_name = natura_pop[0][1]
        else:
            self.site_code = None
            self.site_name = None

        self.description = self.get_description()
        self.impact = self.assess_impact()

        self.table_description = text_templates["natura2000_birds_table_description"]
        self.table = self.query_birds_table()


        self.table_habitats = get_natura_povs(self.point)
        self.tables = [self.table_habitats, self.table]
        # TODO: add "tables", a list of "table" objects

    def get_description(self):
        self.description = natura_description(self.project_title, self.site_code, self.site_name, distance = 5, intersection=True)
        return self.description

    def assess_impact(self):
        self.impact = natura_impact_assessment(self.lat, self.lon, self.project_title, self.project_type)
        return self.impact

    def query_birds_table(self):
        self.birds = session.query(birds_table.c.latin, 
                                   birds_table.c.croatian, 
                                   birds_table.c.Status_G, 
                                   birds_table.c.Status_P, 
                                   birds_table.c.Status_Z).filter_by(code=self.site_code).all()
        return self.birds
    
    # def query_povs(self):
    #     self.site_code = get_natura_povs(self.point)
    #     return self.site_code
    

class ProtectedAreasChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)
        # specific
        self.heading = text_templates["protected_areas_heading"]
        self.table_description = text_templates["protected_areas_table_description"]
        self.table = get_zpp_polygons(self.point)
        self.description = self.get_zpp_description()

    def get_zpp_description(self):
        # protected_areas_description = f"Development project called {self.project_title} is located in some protected areas"
        variables = {
            'project_title': self.project_title
        }
        protected_areas_description = text_templates["protected_areas_description"]
        protected_areas_description = protected_areas_description.format(**variables)

        return protected_areas_description

class AdministrativeChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)
        # specific
        self.heading = text_templates["administrative_heading"]
        self.administrative_zones = get_administrative_cro(self.point)[0][0]
        self.description = self.get_topological_description()


    def get_topological_description(self):
        variables = {
            'project_title': self.project_title,
            'administrative_zones': self.administrative_zones
        }
        administrative_description = text_templates["administrative_description"]
        administrative_description = administrative_description.format(**variables)
        return administrative_description
    

class BiodiversityChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["biodiversity_heading"]
        self.table_meta = text_templates["biodiversity_table_meta"]
        self.table_description = text_templates["biodiversity_table_description"]
        self.table = get_habitats_2016(self.point)
        self.bioregion = text_templates["biodiversity_bioregion"]
        self.description = self.get_habitat_description()

    def get_habitat_description(self):
        # biodiversity_description = f"The habitats found on site of {self.project_title} are charasteristic for {self.bioregion} biogeoregion"
        variables = {
            "project_title": self.project_title,
            "bioregion": self.bioregion
        }
        biodiversity_description = text_templates["biodiversity_description"]
        biodiversity_description = biodiversity_description.format(**variables)

        return biodiversity_description
    

class ForestChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["forests_heading"]
        self.table_meta = text_templates["forests_table_meta"]
        self.table_description = text_templates["forests_table_description"]

        self.forest_gj = get_forest_private_gj(self.point)[0]
        self.table = get_forest_private_unit(self.point)
        self.description = self.get_forestry_description()

    def get_forestry_description(self) -> str:
        variables = {
            "project_title": self.project_title,
            "forest_gj": f"{self.forest_gj[1]} - {self.forest_gj[0]}"
        }
        forests_description = text_templates["forests_description"]
        forests_description = forests_description.format(**variables)
                                                                   
        return forests_description
    

class ClimateChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["climate_heading"]
        self.climate_zones = "CLimate zones are Abcdf"
        self.description = self.get_climate_description()
            
    def get_climate_description(data):
        return climate_analysis_of_probability.result_text
    

class GeologyChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["geology_heading"]
        self.administrative_zones = get_administrative_cro(self.point)
        self.description = self.get_topological_description()

    def get_topological_description(self):
        geology_description = f"Development project called {self.project_title} is located administratively in {self.administrative_zones}"
        return geology_description
    
class HidrologyChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["hidrology_heading"]
        self.table = get_esri_water_bodies(self.point)
        self.description = self.get_hidrology_description()

    def get_hidrology_description(self):
        variables = {
            "project_title": self.project_title
        }

        hidrology_description = text_templates["hidrology_description"]
        hidrology_description = hidrology_description.format(**variables)
        return hidrology_description
    
class LandscapeChapter(Chapter):
    def __init__(self, project_title, project_type, project_id, lat, lon) -> None:

        # TODO: One-to-many relationship between project and chapters
        # redundant stuff for now
        self.lat = lat
        self.lon = lon
        self.project_title = project_title
        self.project_type = project_type
        self.point = create_point(lat, lon)

        # specific
        self.heading = text_templates["landscape_heading"]
        self.landscape_type = text_templates["landscape_type"]
        self.culture = text_templates["landscape_culture"]
        self.description = self.get_landscape_description()

    def get_landscape_description(self):
        variables = {
                    "landscape_type": self.landscape_type,
                    "culture": self.culture
                }
        landscape_description = text_templates["landscape_description"]
        landscape_description = landscape_description.format(**variables)
        return landscape_description

@login.user_loader
def load_user(id):
    return User.query.get(int(id))