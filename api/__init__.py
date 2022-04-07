from flask import Blueprint, request


bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/tik', methods=['POST'])
def tik():
    data = request.json
    return data
