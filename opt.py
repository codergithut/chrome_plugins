from functools import wraps

import flask_restful
from flask import request
from flask_restful import reqparse
from jwt import ExpiredSignatureError
import urllib.request

from db import get_db
from jwt_util import jwt_util

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]

## jwt 验证密钥
secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'

## token签名方法
algorithm = 'HS256'

## jwt工具
jwt = jwt_util(secret, algorithm)

## result 结果
result = {"code": 0}

## 表单获取数据
parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('token')
parser.add_argument('remark')


args=[]

## 用户id
user_id=0

## 用户token验证
def basic_authentication():
    args = parser.parse_args()
    token = request.headers.get("Authorization")
    try:
        if jwt.verifToken(token):
            user_id = jwt.verifToken(token)['id']
            return 0
        return 1
    except ExpiredSignatureError as e:
        return 2
    pass

## 用户验证切面
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = basic_authentication()  # custom account lookup function

        if acct == 0:
            return func(*args, **kwargs)

        if acct == 1:
            flask_restful.abort(401)

        if acct == 2:
            flask_restful.abort(402)
    return wrapper

class Resource(flask_restful.Resource):
    method_decorators = [authenticate]
    pass

## 收藏url
class OptSaveUrl(Resource):
    def post(self):
        args = parser.parse_args()
        url = args['url']
        status = check_url(url)
        remark = args['remark']
        tag = 'default'

        if checkUserRecordData():
            db = get_db()
            db.execute(
                'update url_record set remark = ?, tag = ?, status = ? where user_id = ? and url = ?',
                (remark, tag, status, user_id , url)
            )
            db.commit()
            result['message'] = 'update'
            result['code'] = 0
            return result, 201
        else:
            db = get_db()
            db.execute(
                'INSERT INTO url_record (url, user_id, status, remark, tag)'
                ' VALUES (?, ?, ?, ?, ?)',
                (url, user_id, status, remark, tag)
            )
            db.commit()

            result['message'] = 'success'
            result['code'] = 0
            return result, 201
        pass
    pass

def check_url(tempUrl):
    if tempUrl != None:
        return 0
    else:
        return 1
    return 0


## 验证用户是否有url
def checkUserRecordData():
    args = parser.parse_args()
    db = get_db()
    users = db.execute(
        'SELECT user_id '
        ' FROM url_record'
        ' WHERE user_id = ? and url = ?', (user_id,args['url'])
    ).fetchall()
    if users.__len__()>0:
        return True
    else:
        return False
    pass

## 删除用户收藏的url
class OptDeleteUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        if checkUserRecordData():
            db.execute('DELETE FROM url_record WHERE user_id = ? and url = ?', (user_id, args['url']))
            db.commit()
            result['message'] = 'success'
            result['code'] = 0
            return result, 201
        pass
        result['message'] = 'fail'
        result['code'] = 2
        return result, 201
    pass

## 查询用户已收藏的url
class OptSearchUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        urlRecords = urlRecords = db.execute('select url from url_record WHERE user_id = ?', (user_id,))
        db.commit()
        record_urls = []
        for record in urlRecords:
            print(tuple(record)[0])
            record_urls.append(tuple(record)[0])
        result['message'] = 'success'
        result['code'] = 0
        result['data'] = record_urls
        return result, 201
    pass