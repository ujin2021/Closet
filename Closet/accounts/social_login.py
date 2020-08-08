from .models import Account, Clothes_category
from .my_settings import SECRET_KEY, EMAIL

import jwt
from django.http import JsonResponse

def social_login(platform, uid, email):
    platform, uid, email = platform, uid, email
    print('platform : ',  str(platform), 'email:', email, 'uid : ', uid)
    username = email.split('@')[0]

    myuser = Account.objects.filter(email=email)

    if myuser : # 같은 email주소가 있다면(소셜로그인으로 로그인 한 적 있다면)
        pass # db저장 필요없다
    else: # 소셜로그인이 처음이면 -> uid 저장 + user info 저장
        form = Account(platform=platform, email=email, password=uid, is_active=True, username=username)
        form.save()

    myuser = Account.objects.get(email=email)
    token = jwt.encode({'user':myuser.id}, SECRET_KEY['secret'], SECRET_KEY['algorithm']).decode('UTF-8')
    print("token = ", token)
    result = {'token':token}#'raspberryPi':myuser.raspberrypiId
    return result
