from flask import Blueprint, render_template, flash, request, redirect, current_app
from .models import Pos, Manual

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def index():
    pda_logung = Pos.get_by_id(1)
    num_days = 1
    tma_manual = [r for r in pda_logung.manuals.order_by(Manual.sampling.desc()).limit(num_days)]
    return render_template('map/index.html', tma_logung=tma_manual, GMAP_KEY=current_app.config.get('GMAP_KEY'))
