from functools import wraps

import auth
import flask_factory
import opt

t = flask_factory.FlaskFactory()

app = t.app
api = t.api

##
## Actually setup the Api resource routing here
##

api.add_resource(auth.AuthRegister, "/auth/register")
api.add_resource(auth.AuthUnRegister, "/auth/unregister")
api.add_resource(auth.AuthVerifyUserInfo, "/auth/verifyUserInfo")
api.add_resource(opt.OptSaveUrl, "/opt/save")
api.add_resource(opt.OptSearchUrl, "/opt/search")
api.add_resource(opt.OptDeleteUrl, "/opt/delete")


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
    app.cli.get_command("init-db")