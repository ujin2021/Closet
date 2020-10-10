from ..models import *
from ..tokenCheck import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL, CATEGORY
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

class ClothesFrequency(ListView) :
    @LoginConfirm
    def get(self, request) :
        try:
            user_id = request.user.id
            print('request user id : ', user_id)
            freq_image = {'top' : [], 'bottom' : [], 'outer' : [], 'dress' : []}
            media_url = 'http://13.124.208.47:8000/media/'

            result = User_Closet.objects.select_related('clothes').filter(user_id=user_id).values('frequency', 'clothes__category', 'clothes__image')
            print('result : ', result)
            for clothes in result :
                freq_image[CATEGORY[clothes['clothes__category']]].append((clothes['frequency'], clothes['clothes__image']))
            
            freq_image['top'] = sorted(freq_image['top'], key = lambda x : -x[0])
            freq_image['bottom'] = sorted(freq_image['bottom'], key = lambda x : -x[0])
            freq_image['outer'] = sorted(freq_image['outer'], key = lambda x : -x[0])
            freq_image['dress'] = sorted(freq_image['dress'], key = lambda x : -x[0])

            freq_image['top'] = [media_url + x[1] for x in freq_image['top'][:3]]
            freq_image['bottom'] = [media_url + x[1] for x in freq_image['bottom'][:3]]
            freq_image['outer'] = [media_url + x[1] for x in freq_image['outer'][:3]]
            freq_image['dress'] = [media_url + x[1] for x in freq_image['dress'][:3]]

            return JsonResponse({'msg' : 'frequency result', 'freq_url' : freq_image}, status=200)
        except Exception as e : 
            print('Frequency e : ', e)
            return JsonResponse({'msg' : e}, status = 400)
