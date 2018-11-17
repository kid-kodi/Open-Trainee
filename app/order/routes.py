# app/Order/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import OrderForm
from .. import db
from ..models import Order

# Order Views

@bp.route('/order', methods=['GET', 'POST'])
@login_required
def index():
    list = Order.query.all()
    return render_template('order/index.html',
                           list=list, title="order")

@bp.route('/order/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            display_as=form.display_as.data, 
            phone=form.phone.data,
            status=1,
            created_by=current_user.id,
            created_at=datetime.utcnow())
        try:
            # add Order to the database
            db.session.add(order)
            db.session.commit()
            flash('Enregistrement effectué avec succès')
        except:
            # in case Order name already exists
            flash('Cet élement figure deja dans votre base de donnée')

        # redirect to order page
        return redirect(url_for('order.index'))

    # load Order template
    return render_template('order/form.html', action="Add",
                           add=add, form=form,
                           title="Add Order")

@bp.route('/order/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=Order)
    if form.validate_on_submit():
        order.display_as = form.display_as.data
        order.phone = form.phone.data
        order.email = form.email.data
        db.session.commit()
        flash('Modifications effectuées avec succès')

        # redirect to the order page
        return redirect(url_for('order.index'))

    form.display_as.data = order.display_as
    form.phone.data = order.phone
    form.email.data = order.email
    return render_template('order/form.html', action="Edit",
                           add=add, form=form,
                           order=order, title="Edit Order")

@bp.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    order = Order.query.get_or_404(id)
    return render_template('order/detail.html',
                           order=order, title="order")


@bp.route('/order/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a Order from the database
    """

    Order = Order.query.get_or_404(id)
    db.session.delete(Order)
    db.session.commit()
    flash('You have successfully deleted the Order.')

    # redirect to the order page
    return redirect(url_for('Order.list'))