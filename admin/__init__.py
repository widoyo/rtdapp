import datetime
from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..models import User, Pos, Pengungsian, Manual
from ..forms import PosForm, UserForm, ManualForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/pos/<int:id>/edit', methods=['GET', 'POST'])
def edit_pos(id):
    pos = Pos.get_by_id(id)
    if request.method == 'POST':
        form = PosForm(request.form, obj=pos)
        if form.validate():
            form.populate_obj(pos)
            pos.save()
            flash("Sukses edit Pos Hidrologi")
            return redirect('/admin/pos')
        else:
            flash(form.errors)
    else:
        form = PosForm(obj=pos)
    return render_template('/admin/pos/edit.html', pos=pos, form=form)
    
@bp.route('/pos/<int:id>', methods=['GET', 'POST'])
def show_pos(id):
    month = request.args.get('month', datetime.datetime.today().strftime('%Y/%m'))
    if '-' in month:
        month = month.replace('-', '/')
    try:
        t = datetime.datetime.strptime(month, '%Y/%m')
    except:
        t = datetime.datetime.today()
    prev_month = t - datetime.timedelta(days=2)
    next_month = t + datetime.timedelta(days=33)
    pos = Pos.get_by_id(id)
    manual_obj = Manual(pos=pos)
    manual_bulan_ini = Manual.select().where((Manual.pos == pos) 
                                             & (Manual.sampling.year==t.year)
                                             & (Manual.sampling.month==t.month)).order_by(Manual.sampling.desc())
    if request.method == 'POST':
        form = ManualForm(request.form, obj=manual_obj)
        if form.validate():
            form.populate_obj(manual_obj)
            jam = datetime.datetime.strptime(form.jam.data, '%H').time()
            manual_obj.sampling = datetime.datetime.combine(form.tanggal.data, jam)
            manual_obj.save()
            flash("Sukses menambah data Manual")
            return redirect('/admin/pos/1')
        else:
            flash(form.errors)
    else:
        form = ManualForm(obj=manual_obj)
    return render_template('/admin/pos/show.html', pos=pos, 
                           form=form, month=t, 
                           prev_month=prev_month.strftime('%Y/%m'), next_month=next_month.strftime('%Y/%m'),
                           manual_bulan_ini=manual_bulan_ini)


@bp.route('/pos', methods=['GET', 'POST'])
def pos():
    pos_baru = Pos()
    if request.method == 'POST':
        form = PosForm(request.form, obj=pos_baru)
        print(form.data)
        if form.validate():
            form.populate_obj(pos_baru)
            pos_baru.save()
            flash('Sukses menambah %s' % pos_baru.nama, 'success')
            return redirect(url_for('admin.pos'))
    else:
        form = PosForm()
    return render_template('/admin/pos/index.html', poses=Pos.select(), form=form)


@bp.route('/')
def index():
    print('admin')
    return render_template('/admin/index.html')

import rtdapp.admin.users
import rtdapp.admin.pengungsian