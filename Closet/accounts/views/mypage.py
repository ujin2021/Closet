from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL
from ..tokenCheck import *
from ..rasp_socket import sendToken

from django.views.generic import ListView
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from datetime import datetime
now = datetime.now()

class Mypage(ListView):
    @LoginConfirm
    def get(self, request):
        try :
            user_id = request.user.id
            print("request user id: ", user_id)

            user = Account.objects.get(id=user_id)
            rasp = RaspberryPi.objects.filter(user_id=user_id).values('ip', 'port')

            if (len(rasp) == 0) :
                rasp_ip = ''
                rasp_port = ''
            else :
                rasp_ip = rasp[0]['ip']
                rasp_port = rasp[0]['port']

            return JsonResponse({'email' : user.email, 'rasp_ip': rasp_ip, 'rasp_port' : rasp_port}, status=200)
        except Exception as e :
            print('ClothesInfo get e : ', e)
            return JsonResponse(e, safe=False)

    @LoginConfirm
    def post(self,request): # rasp info create & update
        try : 
            user_id = request.user.id
            print("request user id: ", user_id)
            token = request.headers.get("Authorizations", None)

            rasp_ip = request.POST.get('rasp_ip', '')
            rasp_port = request.POST.get('rasp_port', '') 

            user = RaspberryPi.objects.filter(user_id=user_id)

            if (len(user) > 0) : # rasp 정보를 update할 때 -> 이때도 ip, port가 정확한지 확인해봐야 함. 같은 토큰을 다시 보내도 상관없는지?
                rasp = RaspberryPi.objects.get(user_id=user_id)
                rasp.ip = rasp_ip
                rasp.port = rasp_port
                rasp.save()

                return JsonResponse({'msg': 'update ok'}, status=200)
                
            else : # rasp 정보를 처음 등록할 때 -> rasp 로 token 전송
                send_result = sendToken(token=token, ip=rasp_ip, port=rasp_port) # rasp 로 토큰 전송하는 함수
                
                if(send_result) : # 토큰이 라즈베리파이에게 잘 보내지면(ip, port번호가 정확하면)
                    rasp = RaspberryPi(ip=rasp_ip, port=rasp_port, user_id=user_id)
                    rasp.save()
                    return JsonResponse({'msg': 'create ok'}, status=201)
                else : 
                    return JsonResponse({'msg' : 'create fail'}, status=400)

        except Exception as e :
            return JsonResponse({'msg': e}, status=400)