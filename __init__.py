import datetime
import os

from flask import (Flask, abort, current_app, flash, g, jsonify,
                   render_template, request, send_from_directory)
from flask_login import LoginManager, current_user
from peewee import fn
from playhouse.shortcuts import model_to_dict
from telegram import Bot
from flask_wtf import CSRFProtect

from wtforms import fields, form, validators

from config import Config

from .api.error import error_response as api_error_response
from .models import (KATEGORI_SIAGA, KONDISI_SIAGA, SIAGA_LOGUNG, Manual, Pos,
                     StatusLog)

csrf = CSRFProtect()

def send_telegram_ewschannel(msg):
    send_telegram('@ewsbbwspj', msg)
    
def send_telegram(to, msg):
    bot = Bot(current_app.config.get('BBWSPJBOT_TOKEN'))
    bot.sendMessage(to, msg)
    
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.from_mapping(DATABASE='sqlite:///' + os.path.join(app.instance_path, app.config.get('DATABASE_NAME')))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import admin, api, auth, map, rtd
    from .models import User, db
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(rtd.bp)

    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.get_by_id(user_id)
        except:
            return None

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            current_user.save()
            
         
    @app.context_processor
    def inject_today_date():
        return {'today_date': datetime.date.today()}
    

    @app.route('/petunjuk')
    def petunjuk_penggunaan():
        return render_template('user_manual.html')
    

    @app.route('/aplikasi')
    def tentang_aplikasi():
        return render_template('tentang_aplikasi.html')
    
    
    @app.route('/favicon.ico')
    def favicon():
        print(app.root_path)
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'pupr.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/tv')
    def tv_show():
        want_json = request.args.get('json', None)
        allpos = Pos.select()
        pchs = [p for p in allpos if p.tipe == 1]
        pdas = [p for p in allpos if p.tipe == 2]
        if want_json:
            return jsonify({'pdas': [model_to_dict(p) for p in pdas], 'pchs': [model_to_dict(p) for p in pchs]})
        return render_template('tv_show.html', pchs=pchs, pdas=pdas)
    
    
    @app.route('/status')
    def status():
        sts = StatusLog.select().order_by(StatusLog.tanggal.desc())
        sts = [{'tanggal': s.tanggal, 'kategori': dict(KATEGORI_SIAGA)[s.kategori],
                'kategori_id': s.kategori,
                'kondisi': dict(KONDISI_SIAGA)[s.kondisi],
                'catatan': s.catatan} for s in sts]
        return render_template('status.html', statuslog=sts)
    
    
    @app.route('/')
    def home():
        import random
        pda_logung = Pos.get_by_id(1)
        num_days = 30
        tma_manual = [(r.sampling, r.tma) for r in pda_logung.manuals.order_by(Manual.sampling.desc()).limit(num_days)]
        tma_now = tma_manual[0]
        tma_manual = dict(tma_manual)
        tma_data = [(tma_now[0] - datetime.timedelta(days=i), None) for i in range(num_days)]
        tma_data = [(t[0], tma_manual.get(t[0], None)) for t in tma_data]
        def mycol(e):
            return e[0]
        tma_data = sorted(tma_data, key=mycol)

        status_siaga = StatusLog.select(fn.Max(StatusLog.tanggal).alias('tanggal'),
                                        StatusLog.kategori, StatusLog.kondisi).group_by(StatusLog.kategori).order_by(StatusLog.tanggal.desc())
        status_siaga = [{'tanggal': s.tanggal, 'kategori': dict(KATEGORI_SIAGA)[s.kategori], 'kondisi': dict(KONDISI_SIAGA)[s.kondisi]} for s in status_siaga]
        status_ = StatusLog.select(fn.Max(StatusLog.tanggal).alias('tanggal'),
                                        StatusLog.kategori, StatusLog.kondisi).group_by(StatusLog.kategori).order_by(StatusLog.kondisi.desc()).limit(1)
        status_ = [{'tanggal': s.tanggal, 'kategori': dict(KATEGORI_SIAGA)[s.kategori], 'kondisi': dict(KONDISI_SIAGA)[s.kondisi]} for s in status_]
        return render_template('index.html', tma_logung=tma_data, tma_logung_now=tma_now, SIAGA_LOGUNG=SIAGA_LOGUNG, status_siaga=status_siaga, status_=status_[0])

    def wants_json_response():
        return request.accept_mimetypes['application/json'] >= \
            request.accept_mimetypes['text/html']


    @app.errorhandler(404)
    def not_found_error(error):
        if wants_json_response():
            return api_error_response(404)
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        if wants_json_response():
            return api_error_response(403)
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        if wants_json_response():
            return api_error_response(500)
        return render_template('500.html'), 500

    return app

