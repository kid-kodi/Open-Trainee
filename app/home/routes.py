# app/home/views.py
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from . import home
from ..models import User, Trainee, Unit, Department, Level, Spinneret
from .forms import EditProfileForm, SearchForm

basedir = os.path.abspath(os.path.dirname(__file__))

@home.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    #     g.search_form = SearchForm()
    # g.locale = str(get_locale())

@home.route('/')
def dashboard():
    """
    Render the homepage template on the / route
    """
    user = User.query.all()
    trainee = Trainee.query.all()
    return render_template('home/index.html', user=user, trainee=trainee, title="Welcome")


@home.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@home.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)

@home.route("/setup", methods=['GET', 'POST'])
@login_required
def setup():
    if request.method == 'POST':

        def department_init_func(row):
            d = Department(name=row['name'], description=row['description'])
            return d

        def unit_init_func(row):
            d = Department.query.filter_by(name=row['department']).first()
            u = Unit(name=row['name'], description=row['description'], department=d)
            return u

        def level_init_func(row):
            l = Level(name=row['name'], description=row['description'])
            return l

        def spinneret_init_func(row):
            s = Spinneret(name=row['name'], description=row['description'])
            return s

        def trainee_init_func(row):
            level = Level.query.filter_by(name=row['level']).first()
            unit = Unit.query.filter_by(name=row['unit']).first()
            spinneret = Spinneret.query.filter_by(name=row['spinneret']).first()
            c = Trainee()
            c.image_filename = 'default.png'
            c.image_url = os.path.join(basedir, 'app/static/img/trainee_default.png')
            c.registration_number = row['registration_number']
            c.first_name = row['first_name']
            c.last_name = row['last_name']
            c.level = level
            c.unit_id = unit
            c.spinneret = spinneret
            c.school = row['school']
            c.email = row['email']
            c.phone = row['phone']
            c.theme = row['theme']

            print( row )

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Department, Unit, Level, Spinneret, Trainee],
            initializers=[department_init_func, unit_init_func, level_init_func,
             spinneret_init_func, trainee_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return render_template('home/setup.html')


@home.route("/export", methods=['GET'])
@login_required
def doexport():
    return excel.make_response_from_tables(db.session, [Category, Post], "xls")

@home.route("/handson_view", methods=['GET'])
@login_required
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Category, Post], 'home/handsontable.html')
