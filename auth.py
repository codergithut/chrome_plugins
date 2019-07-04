from functools import wraps

from flask_restful import reqparse, abort, Resource

from db import get_db
from jwt_util import jwt_util


def basic_authentication():
    return False
    pass

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('user_id')

secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'

algorithm = 'HS256'

result = {"code": 0}

jwt = jwt_util.jwt_util(secret, algorithm)


class AuthVerifyUserInfo(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        posts = db.execute(
            'SELECT user_id '
        ' FROM user'
        ' WHERE name = ? and password = ? ', (args['username'],args['password'])
        ).fetchall()

        if(posts.__len__()>0):
            userId=0
            for item in posts:
                userId = tuple(item)[0]
                pass
            result['token'] = jwt.createToken(userId, 1800)
            result['message'] = 'success'
            result['code'] = 0
        else:
            result['message'] = 'can not find userinfo'
            result['code'] = 1
            pass
        return result, 201
    pass

class AuthRegister(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        users = db.execute(
            'SELECT user_id '
            ' FROM user'
            ' WHERE name = ?', (args['username'],)
        ).fetchall()

        if users.__len__()>0:
            result['message'] = 'fail'
            result['code'] = 1
            return result, 500
        pass

        db.execute(
            'INSERT INTO user (name, password)'
            ' VALUES (?, ?)',
            (args['name'], args['password'])
        )
        db.commit()
        result['message'] = 'success'
        result['code']=0
        return result, 201
    pass

class AuthUnRegister(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        users = db.execute(
            'SELECT user_id '
            ' FROM user'
            ' WHERE user_id = ?', (args['user_id'],)
        ).fetchall()
        if users.__len__()>0:
            db.execute('DELETE FROM user WHERE user_id = ?', (args['user_id'],))
            db.commit()
            result['message'] = 'success'
            result['code']=0
            return result, 201
        pass
        result['message'] = 'fail'
        result['code']=2
        return result, 201
    pass

