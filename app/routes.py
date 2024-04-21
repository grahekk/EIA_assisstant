from flask import render_template, flash, redirect, url_for, request, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EmptyForm, ContactForm, NewProjectForm, EditProjectForm, DeleteProjectForm, GeolocationForm
from app.models import User, Post, Questions, Project, query_all, NaturaChapter, AdministrativeChapter, BiodiversityChapter, ForestChapter, LandscapeChapter, ProtectedAreasChapter, HidrologyChapter, ClimateChapter, session, GeoFile
from sqlalchemy.sql import text
from geoalchemy2.functions import ST_AsText, ST_Transform
from werkzeug.utils import secure_filename
from shapely.geometry import shape
from shapely import to_geojson, from_wkb, from_wkt
import geojson

from datetime import datetime
from urllib.parse import urlsplit

from .tools.geoanalysis import get_geodataframe_for_point, create_point
from .tools.plot_map import export_map_with_shapefile
from .tools.report_creation import create_report
from .tools.docx_report import report_from_docx_template
import os
import yaml

# Load YAML data
with open('app/text_templates.yaml', 'r') as file:
    templates = yaml.safe_load(file)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'gpkg', 'geojson', 'shp', 'kml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Add templates to the context
@app.context_processor
def inject_templates():
    return dict(templates=templates)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, 
                           posts=posts.items, next_url=next_url, projects = projects,
                           prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', title='Forgot password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

from app.forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username).first()
        question = Questions(user_id=user.id, title=form.title.data, message = form.text_message.data)
        db.session.add(question)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('contact.html', title='Contact',
                           form=form)

@login_required
@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    project_form = NewProjectForm()
    if project_form.validate_on_submit():
        project = Project(user_id=current_user.id, 
                          project_title=project_form.project_title.data, 
                          description = project_form.description.data,
                          project_type = project_form.project_type.data,
                          lat = project_form.lat.data,
                          lon = project_form.lon.data)
        db.session.add(project)
        db.session.commit()
        flash('Your changes have been saved. Click down below on your project to see the impacts!')
        return redirect(url_for('index'))
    return render_template('new_project.html', title='New project',
                        form=project_form)

@login_required
@app.route('/update_project/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    project_form = EditProjectForm()
    if project_form.validate_on_submit():
        project.project_title = project_form.project_title.data
        project.summary = project_form.summary.data
        project.description = project_form.description.data
        project.project_type = project_form.project_type.data
        project.lat = project_form.lat.data
        project.lon = project_form.lon.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        project_form.project_title.data = project.project_title
        project_form.project_type.data = project.project_type
        # project_form.report_type.data = project.report_type
        project_form.description.data = project.description
        project_form.lat.data = project.lat
        project_form.lon.data = project.lon

        project.impact = project.assess_impact()
        # project_form.impact = project.impact

        natura_chapter = NaturaChapter(project.project_title,
                                       project.project_type,
                                       project_id,
                                       project.lat,
                                       project.lon)
        natura_chapter.table_columns = ["latin", "croatian", "status_g", "status_p", "status_z"]
        
        administrative_chapter = AdministrativeChapter(project.project_title,
                                                       project.project_type,
                                                       project_id,
                                                       project.lat, 
                                                       project.lon)
        
                
        biodiversity_chapter = BiodiversityChapter(project.project_title,
                                                    project.project_type,
                                                    project_id,
                                                    project.lat, 
                                                    project.lon)
        
        
        protected_areas_chapter = ProtectedAreasChapter(project.project_title,
                                                    project.project_type,
                                                    project_id,
                                                    project.lat, 
                                                    project.lon)
        protected_areas_chapter.table_columns = ["kategorija", "naziv", "udaljenost"]
        
        
        forest_chapter = ForestChapter(project.project_title,
                                        project.project_type,
                                        project_id,
                                        project.lat, 
                                        project.lon)
        
        landscape_chapter = LandscapeChapter(project.project_title,
                                project.project_type,
                                project_id,
                                project.lat, 
                                project.lon)
        
        hidrology_chapter = HidrologyChapter(project.project_title,
                                project.project_type,
                                project_id,
                                project.lat, 
                                project.lon)
        
        climate_chapter = ClimateChapter(project.project_title,
                                project.project_type,
                                project_id,
                                project.lat, 
                                project.lon)
        
        project.chapters = [administrative_chapter, 
                            natura_chapter, 
                            biodiversity_chapter, 
                            protected_areas_chapter, 
                            hidrology_chapter, 
                            forest_chapter, 
                            landscape_chapter, 
                            climate_chapter]


        results = query_all(create_point(project.lat, project.lon))
        labels = [
        "POVS",
        "POP",
        "Administrative zone",
        "Habitats from 2004 map",
        "Habitats from 2016 map",
        "MAB",
        "Protected areas - points",
        "Protected areas - polygons",
        "Forests - private areas",
        "Forest private units",
        "Water bodies",
        "Small rivers",
        "Bigger rivers - polygons"
        ]
        
        # for r in results.items():
        #     print(r)

        # Get the template from YAML
        template = templates.get('project_location', '')
        # Substitute placeholders with actual values
        result_text = template.format(project=project.project_title, lat=project.lat, lon=project.lon)

        if project.geo_files:
            # transform wkb to geojson
            geometry = from_wkt(db.session.scalar(ST_AsText(project.geo_files.geometry)))
            project.geojson_data = to_geojson(geometry)

    return render_template('update_project.html', title='Update project',
                        form=project_form, project = project)   

@login_required
@app.route('/delete/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    project_name = project.project_title
    project_form = DeleteProjectForm()
    if project_form.validate_on_submit():

        db.session.execute(text(f"DELETE FROM project WHERE id={project_id}"))
        db.session.commit()

        flash(f'Your project "{project_name}" has been deleted.')
        return redirect(url_for('index'))

    elif request.method == 'GET':    
        return render_template('delete_project.html', title='Delete project',
                            form=project_form, project = project)
    
@login_required
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def dashboard():
    projects = Project.query.all()
    users = User.query.all()
    page = request.args.get('page', 1, type=int)
    return render_template('admin_dashboard.html', title='Dashboard', 
                          projects = projects, users=users)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@login_required
@app.route('/update_project/download_report/<project_id>', methods=['GET', 'POST'])
def download_report(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()

    #get table
    # project.birds = project.query_birds_table()
    #get shape for map
    natura_chapter = NaturaChapter(project.project_title,
                                       project.project_type,
                                       project_id,
                                       project.lat,
                                       project.lon)
    natura_chapter.table_columns = ["latin", "croatian", "status_g", "status_p", "status_z"]
    
    administrative_chapter = AdministrativeChapter(project.project_title,
                                                project.project_type,
                                                project_id,
                                                project.lat, 
                                                project.lon)
    
            
    biodiversity_chapter = BiodiversityChapter(project.project_title,
                                                project.project_type,
                                                project_id,
                                                project.lat, 
                                                project.lon)
    
    
    protected_areas_chapter = ProtectedAreasChapter(project.project_title,
                                                project.project_type,
                                                project_id,
                                                project.lat, 
                                                project.lon)
    protected_areas_chapter.table_columns = ["kategorija", "naziv", "udaljenost"]
    
    
    forest_chapter = ForestChapter(project.project_title,
                                    project.project_type,
                                    project_id,
                                    project.lat, 
                                    project.lon)
    
    landscape_chapter = LandscapeChapter(project.project_title,
                            project.project_type,
                            project_id,
                            project.lat, 
                            project.lon)
    
    hidrology_chapter = HidrologyChapter(project.project_title,
                            project.project_type,
                            project_id,
                            project.lat, 
                            project.lon)
    
    climate_chapter = ClimateChapter(project.project_title,
                            project.project_type,
                            project_id,
                            project.lat, 
                            project.lon)
    
    project.chapters = [administrative_chapter, 
                        natura_chapter, 
                        biodiversity_chapter, 
                        protected_areas_chapter, 
                        hidrology_chapter, 
                        forest_chapter, 
                        # landscape_chapter, 
                        climate_chapter]



    pop_gdf = get_geodataframe_for_point(project.lat, project.lon, session)
    # create map image for report
    image_path = "map_image.jpg"
    export_map_with_shapefile(project.lat, project.lon, gdf = pop_gdf, file_path = image_path)
    report = "report.docx"
    report_from_docx_template(project, report) 
    # TODO: do the temporary directory for storing reports (tempfile)
    #create report
    # natura_chapter = NaturaChapter(project.project_title,
    #                                     project.project_type,
    #                                     project_id,
    #                                     project.lat,
    #                                     project.lon)


    # create_report(project.project_title, 
    #               project.impact, 
    #               natura_chapter.table,
    #               image_path, 
    #               report)


    return send_file(os.path.abspath(report))

# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_project/<project_id>/upload_file/', methods=['GET','POST'])
def upload_file(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Convert GeoJSON data to Shapely geometry
            # geojson_data = file.read()
            # geometry = shape(json.loads(geojson_data)['geometry'])

            with open(file_path) as f:
                gj = geojson.load(f)
            features = gj['features'][0]

            shapely_geometry = shape(features["geometry"])
            wkt_geometry = shapely_geometry.wkt

            geo_file = GeoFile(filename=filename, geometry=wkt_geometry)

            # project.geo_files.append(geo_file)
            project.geo_files = geo_file
            db.session.add(geo_file)
            db.session.commit()

            return redirect(url_for('update_project', project_id=project_id))
        
        elif not allowed_file(file.filename):
            flash('The file is not valid, try with .geojson')
            return redirect(request.url)
    
    # render the upload page
    elif request.method == "GET": 
        return render_template("upload_file.html")