import jwt


def decode_jwt(token):
    
        decoded = jwt.decode(token, 'D2DE17E9AE96981973A39FA722F96', algorithms=["HS256"])
        return decoded
   