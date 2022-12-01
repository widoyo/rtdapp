from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..models import Pengungsian
from ..forms import PosForm, UserForm, PengungsianForm
from ..admin import bp, admin_only 


@bp.route('/pengungsian', methods=['GET', 'POST'])
def pengungsian():
    admin_only()
    form = PengungsianForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            obj = Pengungsian()
            form.populate_obj(obj)
            obj.save()
            return obj.nama
        else:
            return form.errors
    return render_template('/admin/pengungsian/index.html', form=PengungsianForm(), poses=Pengungsian.select())
