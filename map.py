from flask import Blueprint, render_template, flash, request, redirect, current_app

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def index():
    return render_template('map/index.html', GMAP_KEY=current_app.config.get('GMAP_KEY'))
