from flask import Blueprint, request

from rtdapp.models import db

bp = Blueprint('api', __name__, url_prefix='/api')


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
