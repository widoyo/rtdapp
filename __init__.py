import os
import datetime
from flask import Flask, render_template, flash, request, send_from_directory, jsonify, current_app
from flask_login import LoginManager, current_user
from wtforms import form, fields, validators
from playhouse.shortcuts import model_to_dict
from telegram import Bot

from .models import Pos, Manual, SIAGA_LOGUNG
from .api.error import error_response as api_error_response
from config import Config

def send_telegram(msg):
    bot = Bot(current_app.config.get('BBWSPJBOT_TOKEN'))
    bot.sendMessage('@widoyoph', msg)
    

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.from_mapping(DATABASE='sqlite:///' + os.path.join(app.instance_path, app.config.get('DATABASE_NAME')))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from .models import db, User
    from . import auth
    from . import admin
    from . import api
    from . import map
    from . import rtd
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(rtd.bp)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

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
        return {'today_date': datetime.datetime.today()}
    
    
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
        return render_template('status.html')
    
    
    @app.route('/')
    def home():
        pda_logung = Pos.get_by_id(1)
        tma_manual = pda_logung.manuals.order_by(Manual.sampling.desc()).limit(2)
        return render_template('index.html', tma_logung=tma_manual, SIAGA_LOGUNG=SIAGA_LOGUNG)

    def wants_json_response():
        return request.accept_mimetypes['application/json'] >= \
            request.accept_mimetypes['text/html']


    @app.errorhandler(404)
    def not_found_error(error):
        if wants_json_response():
            return api_error_response(404)
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_error(error):
        if wants_json_response():
            return api_error_response(500)
        return render_template('500.html'), 500

    return app

