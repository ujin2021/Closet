from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL
from ..tokenCheck import *
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

            rasp_ip = request.POST.get('rasp_ip', '')
            rasp_port = request.POST.get('rasp_port', '') 

            user = RaspberryPi.objects.filter(user_id=user_id)

            if (len(user) > 0) :
                rasp = RaspberryPi.objects.get(user_id=user_id)
                rasp.ip = rasp_ip
                rasp.port = rasp_port
                rasp.save()
                return JsonResponse({'msg': 'update ok'}, status=200)

            else :
                rasp = RaspberryPi(ip=rasp_ip, port=rasp_port, user_id=user_id)
                rasp.save()
                return JsonResponse({'msg': 'create ok'}, status=201)

        except Exception as e :
            return JsonResponse({'msg': e}, status=400)