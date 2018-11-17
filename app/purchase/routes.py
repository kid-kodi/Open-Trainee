# app/Purchase/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import PurchaseForm
from .. import db
from ..models import Purchase

# Purchase Views

@bp.route('/purchase', methods=['GET', 'POST'])
@login_required
def index():
    list = Purchase.query.all()
    return render_template('purchase/index.html',
                           list=list, title="purchase")

@bp.route('/purchase/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = PurchaseForm()
    if form.validate_on_submit():
        purchase = Purchase(
            display_as=form.display_as.data, 
            phone=form.phone.data,
            status=1,
            created_by=current_user.id,
            created_at=datetime.utcnow())
        try:
            # add Purchase to the database
            db.session.add(purchase)
            db.session.commit()
            flash('Enregistrement effectué avec succès')
        except:
            # in case Purchase name already exists
            flash('Cet élement figure deja dans votre base de donnée')

        # redirect to purchase page
        return redirect(url_for('purchase.index'))

    # load Purchase template
    return render_template('purchase/form.html', action="Add",
                           add=add, form=form,
                           title="Add Purchase")

@bp.route('/purchase/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    purchase = Purchase.query.get_or_404(id)
    form = PurchaseForm(obj=Purchase)
    if form.validate_on_submit():
        purchase.display_as = form.display_as.data
        purchase.phone = form.phone.data
        purchase.email = form.email.data
        db.session.commit()
        flash('Modifications effectuées avec succès')

        # redirect to the purchase page
        return redirect(url_for('purchase.index'))

    form.display_as.data = purchase.display_as
    form.phone.data = purchase.phone
    form.email.data = purchase.email
    return render_template('purchase/form.html', action="Edit",
                           add=add, form=form,
                           purchase=purchase, title="Edit Purchase")

@bp.route('/purchase/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    purchase = Purchase.query.get_or_404(id)
    return render_template('purchase/detail.html',
                           purchase=purchase, title="purchase")


@bp.route('/purchase/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a Purchase from the database
    """

    Purchase = Purchase.query.get_or_404(id)
    db.session.delete(Purchase)
    db.session.commit()
    flash('You have successfully deleted the Purchase.')

    # redirect to the purchase page
    return redirect(url_for('Purchase.list'))