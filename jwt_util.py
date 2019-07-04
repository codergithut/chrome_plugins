import jwt
import time

class jwt_util:

    def __init__(self, secret, algorithm):
        self.secret = secret
        self.algorithm = algorithm


    def createToken(self, userId, expire_time):
        return str(jwt.encode({'id': userId, 'exp': time.time() + expire_time}, self.secret, algorithm=self.algorithm), encoding='ascii')

    def verifToken(self, token):
        return jwt.decode(token, self.secret, algorithm=self.algorithm)