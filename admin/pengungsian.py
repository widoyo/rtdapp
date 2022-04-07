from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..models import Pengungsian
from ..forms import PosForm, UserForm
from ..admin import bp 


@bp.route('/pengungsian')
def pengungsian():
    return render_template('/admin/pengungsian/index.html', poses=Pengungsian.select())
