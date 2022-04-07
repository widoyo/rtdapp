from flask import Blueprint, render_template, flash, request, redirect, url_for

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def index():
    return render_template('map/index.html')
