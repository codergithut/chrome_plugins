from functools import wraps

import flask_restful
from flask_restful import reqparse, abort, Resource

from google_plugins.plugin import jwt_util
from google_plugins.plugin.db import get_db
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def basic_authentication():
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
parser.add_argument('task')
parser.add_argument('name')
parser.add_argument('password')

secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'

algorithm = 'HS256'

jwt = jwt_util.jwt_util(secret, algorithm)

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            ("haha", "ssss", 1)
        )
        db.commit()

        db = get_db()
        posts = db.execute(
            'select author_id from post'
        ).fetchall()

        result = {"code": 0, "msg": "sucess"}

        result1 = ResponseMessage("test");


        for item in posts:
            # L.append(item.__dict__)
            print(tuple(item)[0])
            tuple(item)
            pass
        result['data'] = "this is test"
        return result


    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    pass
pass


class AuthVerifyUserInfo(Resource):
    def post(self):
        args = parser.parse_args()
        return "AuthVerifyUserInfo", 201
    pass

class AuthRegister(Resource):
    def post(self):
        args = parser.parse_args()
        return "AuthRegister", 201
    pass

class AuthUnRegister(Resource):
    def post(self):
        args = parser.parse_args()
        return "AuthUnRegister", 201
    pass

class AuthVerifyToken(Resource):

    def post(self):
        result = {"code": 0}
        args = parser.parse_args()
        db = get_db()
        posts = db.execute(
            'SELECT user_id '
        ' FROM user'
        ' WHERE name = ? and password = ? ', (args['name'],args['password'])
        ).fetchall()

        if(posts.__len__()>0):
            userId=0
            for item in posts:
                userId = tuple(item)[0]
                pass
            result['token'] = jwt.createToken(userId, 1800)
            result['message'] = 'success'
        else:
            result['message'] = 'can not find userinfo'
            result['code'] = 1
            pass
        return result, 201

    pass

class OptSaveUrl(Resource):
    def post(self):
        args = parser.parse_args()
        return "OptSaveUrl", 201

class OptDeleteUrl(Resource):
    def post(self):
        args = parser.parse_args()
        return "OptDeleteUrl", 201

class ResponseMessage():
    def __init__(self, name) :
        self.name = name;
