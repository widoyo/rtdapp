from flask import Blueprint, request, jsonify
from peewee import fn
from rtdapp.models import db, StatusLog, KATEGORI_SIAGA, KONDISI_SIAGA

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('status')
def status():
    status_siaga = StatusLog.select(fn.Max(StatusLog.tanggal).alias('tanggal'),
                                    StatusLog.kategori, StatusLog.kondisi).group_by(StatusLog.kategori).order_by(StatusLog.kondisi.desc()).limit(1)
    status_siaga = [{'tanggal': s.tanggal, 'kategori': dict(KATEGORI_SIAGA)[s.kategori], 'kondisi': dict(KONDISI_SIAGA)[s.kondisi]} for s in status_siaga]
    return jsonify(status_siaga)

@bp.route('update', methods=['POST'])
def update():
    data = request.form
    if data.get('obj') not in ['pengungsian', 'manual']:
        return "obj tidak valid", 400
    table = data.get('obj')
    field = data.get('name')
    oid = data.get('pk')
    val = data.get('value')
    sql = "UPDATE {table} set {nama}='{nilai}' WHERE id={oid}".format(table=table, 
                                                                nama=field, 
                                                                nilai=val, 
                                                                oid=oid)
    db.database.execute_sql(sql)    
    return sql, 200

@bp.route('/tik', methods=['POST'])
def tik():
    data = request.json
    return data
