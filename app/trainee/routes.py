# app/trainee/views.py
import os
from flask import abort, flash, request, redirect, render_template, url_for, jsonify
#from flask_weasyprint import HTML, render_pdf
from flask_login import current_user, login_required

from . import trainee
from .forms import TraineeForm, SearchForm
from .. import db, images
from ..models import Trainee, Level, Spinneret, Unit, User, Department

import flask_excel as excel
from datetime import datetime
from flask_weasyprint import HTML, render_pdf

basedir = ''

from sqlalchemy.sql.expression import and_


def get_query(table, lookups, form_data):
    conditions = [
        getattr(table, field_name) == form_data[field_name]
        for field_name in lookups if form_data[field_name]
    ]

    return table.query.filter(and_(*conditions))

#routes order
@trainee.route('/trainees', methods=['GET', 'POST'])
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    #form.unit_id.choices = [(c.id, c.name) for c in Unit.query.all()]
    form.unit_id.choices.append((0,'All unit'))
    for unit in Unit.query.all():
        form.unit_id.choices.append((unit.id, unit.name))

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        unit_id = form.unit_id.data
        print(type(unit_id))
        print(unit_id!=0)
        query = Trainee.query
        if first_name:
            query = query.filter(Trainee.first_name == first_name)
        elif last_name:
            query = query.filter(Trainee.last_name == last_name)
        elif unit_id > 0:
            query = query.filter(Trainee.unit_id == unit_id)

        pagination = query.order_by(Trainee.created_at.desc()).paginate(
            page, per_page=25,
            error_out=False)
    else:
        pagination = Trainee.query.order_by(Trainee.created_at.desc()).paginate(
            page, per_page=25,
            error_out=False)

    _list = pagination.items
    return render_template('trainee/list.html', list=_list, form=form, pagination=pagination)


@trainee.route('/trainees/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a trainee to the database
    """

    add = True

    form = TraineeForm()
    form.level_id.choices = [(lvl.id, lvl.name) for lvl in Level.query.all()]
    form.spinneret_id.choices = [(sp.id, sp.name) for sp in Spinneret.query.all()]
    form.unit_id.choices = [(u.id, u.name) for u in Unit.query.all()]
    if form.validate_on_submit():
        if 'image' in request.files:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            print('file exist')
        else:
            print('file do not exist')
            filename = 'default.png'
            url = os.path.join( basedir, '/static/img/default.png')

        trainee = Trainee(registration_number=generateNum(),
            image_filename=filename,
            image_url=url,
            level_id=form.level_id.data,
            spinneret_id=form.spinneret_id.data,
            unit_id=form.unit_id.data,
            school=form.school.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            birthdate=form.birthdate.data,
            diplome=form.diplome.data,
            responsable=form.responsable.data,
            started_date=form.started_date.data,
            ended_date=form.ended_date.data,
            apply_date=form.apply_date.data,
            phone=form.phone.data,
            theme=form.theme.data)
        try:
            # add trainee to the database
            db.session.add(trainee)
            db.session.commit()
            flash('You have successfully added a new trainee.')
        except:
            # in case trainee name already exists
            flash('Error: trainee name already exists.')

        # redirect to trainees page
        return redirect(url_for('trainee.list'))

    # load trainee template
    return render_template('trainee/form.html', action="Add",
                           add=add, form=form,
                           title="Add Trainee")

@trainee.route('/trainees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit a trainee
    """

    add = False

    trainee = Trainee.query.get_or_404(id)
    form = TraineeForm(obj=trainee)
    form.level_id.choices = [(lvl.id, lvl.name) for lvl in Level.query.all()]
    form.spinneret_id.choices = [(sp.id, sp.name) for sp in Spinneret.query.all()]
    form.unit_id.choices = [(u.id, u.name) for u in Unit.query.all()]
    if form.validate_on_submit():
        if 'image' in request.files:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            trainee.image_filename = filename
            trainee.image_url = url

        trainee.school = form.school.data
        trainee.level_id = form.level_id.data
        trainee.spinneret_id = form.spinneret_id.data
        trainee.unit_id = form.unit_id.data
        trainee.first_name = form.first_name.data
        trainee.last_name = form.last_name.data
        trainee.email = form.email.data
        trainee.phone = form.phone.data
        trainee.theme = form.theme.data
        trainee.birthdate = form.birthdate.data
        trainee.diplome = form.diplome.data
        trainee.responsable=form.responsable.data
        trainee.started_date=form.started_date.data
        trainee.ended_date=form.ended_date.data
        trainee.apply_date=form.apply_date.data
        db.session.commit()
        flash('You have successfully edited the trainee.')

        # redirect to the trainees page
        return redirect(url_for('trainee.list'))

    form.level_id.data = trainee.level_id
    form.spinneret_id.data = trainee.spinneret_id
    form.unit_id.data = trainee.unit_id
    form.first_name.data = trainee.first_name
    form.last_name.data = trainee.last_name
    form.email.data = trainee.email
    form.phone.data = trainee.phone
    form.birthdate.data = trainee.birthdate
    form.theme.data = trainee.theme
    form.diplome.data = trainee.diplome
    form.responsable.data = trainee.responsable
    form.started_date.data = trainee.started_date
    form.ended_date.data = trainee.ended_date
    form.apply_date.data = trainee.apply_date
    return render_template('trainee/form.html', action="Edit",
                           add=add, form=form,
                           trainee=trainee, title="Edit Trainee")

@trainee.route('/trainees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a trainee from the database
    """

    trainee = Trainee.query.get_or_404(id)
    db.session.delete(trainee)
    db.session.commit()
    flash('You have successfully deleted the trainee.')

    # redirect to the trainees page
    return redirect(url_for('trainee.list'))


@trainee.route("/trainee/import", methods=['GET', 'POST'])
@login_required
def import_in():
    if request.method == 'POST':

        def level_init(row):
            l = Level()
            num = Level.query.filter_by(name=row['Nom']).count()
            if num == 0 :
                l.name = row['Nom']
                l.description = row['Description']
            return l

        def spinneret_init(row):
            s = Spinneret()
            num = Spinneret.query.filter_by(name=row['Nom']).count()
            if num == 0 :
                s.name = row['Nom']
                s.description = row['Description']
            return s


        def department_init(row):
            s = Department()
            num = Department.query.filter_by(name=row['Nom']).count()
            print(str(num))
            if num == 0 :
                s.name = row['Nom']
                s.description = row['Description']
            return s

        def unit_init(row):
            s = Unit()
            num = Unit.query.filter_by(name=row['Nom']).count()
            if num == 0 :
                s.name = row['Nom']
                s.description = row['Description']
                d = Department.query.filter_by(name=row['Departement']).first()
                s.departement_id = d.id
            return s

        def trainee_init(row):
            c = Trainee()
            c.image_filename = 'default.png'
            c.image_url = os.path.join('', '/static/img/default.png')
            c.registration_number = row['Numero']
            c.first_name = row['Nom']
            c.last_name = row['Prenoms']

            l = Level.query.filter_by(name=row['Niveau']).first()
            c.level_id = l.id

            u = Unit.query.filter_by(name=row['Unite']).first()
            c.unit_id = u.id

            s = Spinneret.query.filter_by(name=row['Filiere']).first()
            c.spinneret_id = s.id

            c.school = row['Etablissement']
            c.email = row['Email']
            c.phone = row['Telephone']
            c.birthdate = row['Date de naissance']
            c.diplome = row['Diplome']
            c.theme = row['Theme']
            return c

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Department, Unit, Spinneret, Level, Trainee],
            initializers=[department_init, unit_init, spinneret_init, level_init, trainee_init])
        return redirect(url_for('trainee.list'))
    return render_template('trainee/import.html', trainee=trainee)


@trainee.route("/trainee/export", methods=['GET'])
@login_required
def export_out():
    list = Trainee.query.all()
    column_names = ['registration_number', 'first_name', 'last_name', 'level_id', 'unit_id',
                    'school', 'email', 'phone', 'theme']
    return excel.make_response_from_query_sets(list, column_names, "xls", file_name="trainee_data")


@trainee.route("/trainee/download", methods=['GET'])
@login_required
def download():
    return excel.make_response_from_array([['registration_number', 'first_name', 'last_name', 'level_id', 'unit_id',
                    'school', 'email', 'phone', 'theme']],
                                          "xls", file_name="trainee_samples")

@trainee.route('/trainee/print', methods=['GET', 'POST'])
@login_required
def print_to():
    data = request.get_json()
    ids = data['items']
    print( data['items'] )
    trainees = Trainee.query.filter(Trainee.id.in_(ids)).all()
    for value in trainees:
        print( value)
    # Make a PDF straight from HTML in a string.
    return jsonify({ 'trainees': [trainee.to_json() for trainee in trainees] })


@trainee.route('/trainee/pdf', methods=['GET', 'POST'])
@login_required
def pdf():
    name = 'kone'
    # Make a PDF straight from HTML in a string.
    html = render_template('trainee/pdf.html', name=name)
    return render_pdf(HTML(string=html))


def generateNum() :
    now = datetime.utcnow()
    year = now.year
    number = str(year)[-2:] + 'ST-' + str(Trainee.query.count()+1).zfill(4)
    return number