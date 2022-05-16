from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..models import Pengungsian
from ..forms import PosForm, UserForm
from ..admin import bp, admin_only 


@bp.route('/pengungsian')
def pengungsian():
    admin_only()
    return render_template('/admin/pengungsian/index.html', poses=Pengungsian.select())
