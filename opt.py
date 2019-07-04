from functools import wraps

import flask_restful
from flask import request
from flask_restful import reqparse

from db import get_db
from jwt_util import jwt_util

secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'

algorithm = 'HS256'

jwt = jwt_util.jwt_util(secret, algorithm)

def basic_authentication():
    token = request.headers.get("Authorization")
    args = parser.parse_args()
    if jwt.verifToken(token):
        return True
    return False
    pass


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = basic_authentication()  # custom account lookup function

        if acct:
            return func(*args, **kwargs)

        flask_restful.abort(401)
    return wrapper


class Resource(flask_restful.Resource):
    method_decorators = [authenticate]

parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('token')
parser.add_argument('user_id')

secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'

algorithm = 'HS256'

jwt = jwt_util.jwt_util(secret, algorithm)

result = {"code": 0}


class OptSaveUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()

        if checkUserRecordData():
            result['message'] = 'fail'
            result['code'] = 1
            return result, 500
        pass

        db.execute(
            'INSERT INTO url_record (url, user_id)'
            ' VALUES (?, ?)',
            (args['url'], args['user_id'])
        )
        db.commit()
        result['message'] = 'success'
        result['code']=0
        return result, 201
    pass

def checkUserRecordData():
    args = parser.parse_args()
    db = get_db()
    users = db.execute(
        'SELECT user_id '
        ' FROM url_record'
        ' WHERE user_id = ? and url = ?', (args['user_id'],args['url'])
    ).fetchall()
    if users.__len__()>0:
        return True
    else:
        return False
    pass

class OptDeleteUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        if checkUserRecordData():
            db.execute('DELETE FROM url_record WHERE user_id = ? and url = ?', (args['user_id'], args['url']))
            db.commit()
            result['message'] = 'success'
            result['code'] = 0
            return result, 201
        pass
        result['message'] = 'fail'
        result['code'] = 2
        return result, 201
    pass

