# app/trainee/views.py
import os
from flask import abort, flash, request, redirect, render_template, url_for, jsonify
#from flask_weasyprint import HTML, render_pdf
from flask_login import current_user, login_required

from . import trainee
from .forms import TraineeForm
from .. import db, images
from ..models import Trainee, Level, Spinneret, Unit

import flask_excel as excel

basedir = os.path.abspath(os.path.dirname(__file__))

# Trainee Views

@trainee.route('/trainees', methods=['GET', 'POST'])
@login_required
def list():
    """
    List all trainees
    """

    list = Trainee.query.all()

    return render_template('trainee/list.html',
                           list=list, title="Trainees")

@trainee.route('/trainees/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a trainee to the database
    """

    add = True

    form = TraineeForm()
    form.registration_number.data = "#"
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

        trainee = Trainee(registration_number="#",
            image_filename=filename,
            image_url=url,
            level_id=form.level_id.data,
            spinneret_id=form.spinneret_id.data,
            unit_id=form.unit_id.data,
            school=form.school.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
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
    form.theme.data = trainee.theme
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

        def trainee_init_func(row):
            c = Trainee()
            c.image_filename = 'default.png'
            c.image_url = os.path.join(basedir, 'app/static/img/trainee_default.png')
            c.registration_number = row['registration_number']
            c.first_name = row['first_name']
            c.last_name = row['last_name']
            c.level_id = row['level_id']
            c.unit_id = row['unit_id']
            c.school = row['school']
            c.email = row['email']
            c.phone = row['phone']
            c.theme = row['theme']

            print( row )
            
            #c.created_at = datetime.utcnow()
            #c.created_by = current_user.id
            return c

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Trainee],
            initializers=[trainee_init_func])
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


@trainee.route('/trainees/print', methods=['GET', 'POST'])
@login_required
def process():
    if request.method == 'POST':
        tmp3 = request.form.getlist('trainees[]')
        print(len(tmp3))
        redirect(url_for('trainee.list'))
    return redirect(url_for('trainee.list'))