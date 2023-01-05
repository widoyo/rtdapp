import datetime, os, io
from functools import wraps

from werkzeug.utils import secure_filename
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, current_app, Response)
from flask_login import current_user, login_required
from peewee import fn, DoesNotExist
from playhouse.dataset import DataSet

from ..forms import ManualForm, PosForm, SiagaForm, ArusInformasiForm
from ..models import (KATEGORI_SIAGA, KONDISI_SIAGA, Manual, Pengungsian, Pos,
                      StatusLog, KV)

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_only():
    if current_user.role != 1:
        abort(403)

@bp.route('/arusinfo', methods=['POST'])
def update_arusinfo():
    form = ArusInformasiForm()
    if form.validate_on_submit():
        f = form.img_arus_informasi.data
        fname = secure_filename(f.filename)
        try:
            ai = KV.get(KV.k=='img_arus_informasi')
            old_fname = os.path.join(current_app.root_path, 'static/img', ai.v)
            if os.path.exists(old_fname):
                os.remove(old_fname)
            ai.v = fname
            ai.save()
            f.save(os.path.join(current_app.root_path, 'static/img', fname))
            flash('Sukses update Arus Informasi')
            
        except DoesNotExist:
            ai = None
    print(form.errors)
    return redirect('/admin')
    
@bp.route('/pos/manual/del/<int:id>', methods=['POST'])
def manual_del(id):
    admin_only()
    manual_obj = Manual.get(id)
    manual_obj.delete_instance()
    return redirect('/admin/pos/{}'.format(pos.id))
    
@bp.route('/pos/<int:id>/edit', methods=['GET', 'POST'])
def edit_pos(id):
    admin_only()
    pos = Pos.get_by_id(id)
    if request.method == 'POST':
        form = PosForm(request.form, obj=pos)
        if form.validate():
            form.populate_obj(pos)
            pos.save()
            Pos.to_kml()
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
    do_download = request.args.get('download', None)
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
    if do_download == '1':
        ds = DataSet(current_app.config.get('DATABASE'))
        print('Want Download')
        f = io.StringIO()
        ds.freeze(manual_bulan_ini, file_obj=f)
        return Response(f.getvalue(), 
                        headers={"Content-Disposition": 
                            "attachment; filename={}".format(pos.nama + '_' + str(t.year) + '_' + str(t.month) + '.csv')})        
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
    req_path = request.full_path
    download = manual_bulan_ini.count() > 0 and 'download=1' or ''
    if download:
        if '?' in req_path:
            req_path += '&download=1'
        else:
            req_path += '?download=1'
    else:
        req_path = ''
    return render_template('/admin/pos/show.html', pos=pos, 
                           form=form, month=t, 
                           prev_month=prev_month.strftime('%Y/%m'), next_month=next_month.strftime('%Y/%m'),
                           manual_bulan_ini=manual_bulan_ini, req_path=req_path)


@bp.route('/pos', methods=['GET', 'POST'])
def pos():
    admin_only()
    pos_baru = Pos()
    if request.method == 'POST':
        form = PosForm(request.form, obj=pos_baru)
        #print(form.data)
        if form.validate():
            form.populate_obj(pos_baru)
            pos_baru.save()
            Pos.to_kml()
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
    arusinfo_form = ArusInformasiForm()
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
    return render_template('/admin/index.html', siaga_form=form, status_siaga=status_siaga, arusinfo_form=arusinfo_form)

import rtdapp.admin.pengungsian
import rtdapp.admin.users
