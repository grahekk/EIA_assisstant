from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EmptyForm, ContactForm, NewProjectForm, EditProjectForm, DeleteProjectForm
from app.models import User,Post, Questions, Project
from sqlalchemy.sql import text

from datetime import datetime
from urllib.parse import urlsplit

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
    project_form = NewProjectForm()
    if project_form.validate_on_submit():
        project.project_title = project_form.project_title.data
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
        project_form.description.data = project.description
        project_form.lat.data = project.lat
        project_form.lon.data = project.lon
        project.impact = project.assess_impact()
        project_form.impact = project.impact
        project.birds = project.query_birds()

    return render_template('existing_project.html', title='Update project',
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