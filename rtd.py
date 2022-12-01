from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import KV

bp = Blueprint('rtd', __name__, url_prefix='/rtd')

@bp.route('/')
def index():
    return render_template('rtd/index.html')


@bp.route('/about')
def about():
    return render_template('rtd/about.html')


@bp.route('/indikasi')
def indikasi():
    return render_template('rtd/indikasi.html')


@bp.route('/tanggungjawab')
def tanggungjawab():
    return render_template('rtd/tanggungjawab.html')


@bp.route('/arusinformasi')
def arusinformasi():
    ai = KV.get(KV.k=='img_arus_informasi')
    return render_template('rtd/arusinformasi.html', img_arus_informasi=ai.v)