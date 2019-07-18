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
parser.add_argument('recordId')
parser.add_argument('title')
parser.add_argument('batchRecord', location=['json'],type=dict)
args=[]

## 用户id
user_id=0

## 用户token验证
def basic_authentication():
    args = parser.parse_args()
    token = request.headers.get("Authorization")
    try:
        if jwt.verifToken(token):
            return 0
        return 1
    except ExpiredSignatureError as e:
        return 2
    pass

def getUserId():
    token = request.headers.get("Authorization")
    user_id = jwt.verifToken(token)['id']
    return user_id

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
            flask_restful.abort(403)
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
        title = args['title']
        tag = 'default'

        if checkUserRecordData(url):
            db = get_db()
            db.execute(
                'update url_record set remark = ?, tag = ?, status = ? where user_id = ? and url = ?',
                (remark, tag, status, getUserId() , url)
            )
            db.commit()
            db.commit()
            result['message'] = 'update'
            result['code'] = 0
            return result, 201
        else:
            db = get_db()
            db.execute(
                'INSERT INTO url_record (url, user_id, status, remark, tag, type, url_title)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (url, getUserId(), status, remark, tag, '2', title)
            )
            db.commit()
            result.clear()
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
def checkUserRecordData(url):
    args = parser.parse_args()
    db = get_db()
    users = db.execute(
        'SELECT user_id '
        ' FROM url_record'
        ' WHERE user_id = ? and url = ? and url_title', (getUserId(),url, )
    ).fetchall()
    if users.__len__()>0:
        return True
    else:
        return False
    pass


def checkUserRecordExist():
    args = parser.parse_args()
    db = get_db()
    records = db.execute(
        'SELECT user_id '
        ' FROM url_record'
        ' WHERE user_id = ? and record_id = ?', (getUserId(), args['recordId'])
    ).fetchall()
    if records.__len__() > 0:
        return True
    else:
        return False
    pass

## 删除用户收藏的url
class OptDeleteUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        if checkUserRecordExist():
            db.execute('DELETE FROM url_record WHERE user_id = ? and record_id = ?', (getUserId(), args['recordId']))
            db.commit()
            db.commit()
            result['message'] = 'success'
            result['code'] = 0
            return result, 201
        pass
        result.clear()
        result['message'] = 'fail'
        result['code'] = 2
        return result, 201
    pass

## 查询用户已收藏的url
class OptSearchUrl(Resource):
    def post(self):
        args = parser.parse_args()
        db = get_db()
        urlRecords = urlRecords = db\
            .execute('select url, remark, record_id, url_title from url_record WHERE user_id = ?', (getUserId(),))
        db.commit()
        record_urls = []
        for record in urlRecords:
            detail = {}
            detail['url'] = tuple(record)[0]
            detail['remark'] = tuple(record)[1]
            detail['recordId'] = tuple(record)[2]
            detail['title'] = tuple(record)[3]
            record_urls.append(detail)
            pass
        result.clear()
        result['message'] = 'success'
        result['code'] = 0
        result['data'] = record_urls
        return result, 201
    pass

class OptBatchInsert(Resource):
    ##todo 需要token验证，说实话就是漏洞
    def post(self):
        parser_copy = parser.copy()
        args = parser_copy.parse_args()
        batch_record = args['batchRecord']
        records = batch_record['records']
        for record in records:
            if not checkUserRecordData(record['url']):
                db = get_db()
                db.execute(
                    'INSERT INTO url_record (url, user_id, status, remark, tag, type, url_title)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (record['url'], getUserId(), '0', 'upload', 'default', '1', record['title'])
                )
                db.commit()
            pass
        result.clear()
        result['message'] = 'success'
        result['code'] = 0
        return result, 201
    pass
