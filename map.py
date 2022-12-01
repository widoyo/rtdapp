from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request)

from .models import Manual, Pos

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def index():
    pda_logung = Pos.get_by_id(1)
    try:
        tma_manual = pda_logung.manuals.order_by(Manual.sampling.desc()).limit(1)[0]
    except:
        tma_manual = None
    return render_template('map/index.html', tma_logung=tma_manual, GMAP_KEY=current_app.config.get('GMAP_KEY'))
