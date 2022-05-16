from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required, current_user
from ..models import User, Pos
from ..forms import PosForm, UserForm
from ..admin import bp, admin_only


@bp.route('/user/<int:id>/password', methods=['GET', 'POST'])
def user_setpassword(id):
    admin_only()
    user = User.get_by_id(id)
    if request.method == 'POST':
        user.set_password(request.form.get('password'))
        user.save()
    return render_template('/admin/user/setpassword.html', user=user)
    
@bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def user_edit(id):
    admin_only()
    user = User.get_by_id(id)
    if request.method == 'POST':
        form = UserForm(request.form, obj=user)
        if form.validate():
            form.populate_obj(user)
            user.save()
            flash('Sukses update')
            return redirect(url_for('admin.user'))
    else:
        form = UserForm(obj=user)
    return render_template('/admin/user/edit.html', form=form, user=user)

@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    admin_only()
    user_baru = User()
    if request.method == 'POST':
        form = UserForm(request.form, obj=user_baru)
        if form.validate():
            form.populate_obj(user_baru)
            user_baru.save()
            flash('Sukses menambah %s' % user_baru.username, 'success')
            return redirect(url_for('admin.user'))
    else:
        form = UserForm(obj=user_baru)
    users = User.select()
    return render_template('/admin/user/index.html', users = users, form=form)

