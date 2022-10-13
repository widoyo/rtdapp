import datetime
from functools import wraps
from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required, current_user
from peewee import fn
from ..models import StatusLog, User, Pos, Pengungsian, Manual, KATEGORI_SIAGA, KONDISI_SIAGA
from ..forms import PosForm, UserForm, ManualForm, SiagaForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_only():
    if current_user.role != 1:
        abort(403)

@bp.route('/pos/<int:id>/edit', methods=['GET', 'POST'])
def edit_pos(id):
    admin_only()
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
            return redirect('/admin/pos/{}'.format(pos.id))
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
    admin_only()
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

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    admin_only()
    status_baru = StatusLog(**{'user': current_user.username})
    if request.method == 'POST':
        form = SiagaForm(request.form, obj=status_baru)
        if form.validate():
            form.populate_obj(status_baru)
            status_baru.save()
            flash('Sukses ')
            return redirect('/admin')
        else:
            flash(form.errors)
    else:
        form = SiagaForm(**{'user': current_user.username})
    status_siaga = StatusLog.select(fn.Max(StatusLog.tanggal).alias('tanggal'),
                                    StatusLog.kategori, StatusLog.kondisi).group_by(StatusLog.kategori).order_by(StatusLog.id.desc())
    status_siaga = [{'tanggal': s.tanggal, 'kategori': dict(KATEGORI_SIAGA)[s.kategori], 'kondisi': dict(KONDISI_SIAGA)[s.kondisi]} for s in status_siaga]
    return render_template('/admin/index.html', siaga_form=form, status_siaga=status_siaga)

import rtdapp.admin.users
import rtdapp.admin.pengungsian
