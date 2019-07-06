import jwt
import time

## jwt工具
class jwt_util:

    def __init__(self, secret, algorithm):
        self.secret = secret
        self.algorithm = algorithm
        pass

    ## 创建token
    def createToken(self, userId, expire_time):
        return str(jwt.encode({'id': userId, 'exp': time.time() + expire_time}, self.secret, algorithm=self.algorithm), encoding='ascii')
    pass

    ## 验证token
    def verifToken(self, token):
        return jwt.decode(token, self.secret, algorithm=self.algorithm)