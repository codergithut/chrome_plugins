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

## 服务路由服务

#用户注册
api.add_resource(auth.AuthRegister, "/auth/register")

#用户注销
api.add_resource(auth.AuthUnRegister, "/auth/unregister")

#用户验证
api.add_resource(auth.AuthVerifyUserInfo, "/auth/verifyUserInfo")

#用户收藏url
api.add_resource(opt.OptSaveUrl, "/opt/save")

#查询已收藏的url
api.add_resource(opt.OptSearchUrl, "/opt/search")

#删除用户收藏的网页
api.add_resource(opt.OptDeleteUrl, "/opt/delete")


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
    app.cli.get_command("init-db")