from ..models import *
from ..tokenCheck import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL, CATEGORY
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

class MyClothes(ListView) :
    @LoginConfirm
    def post(self, request) :
        try:
            user_id = request.user.id
            print('request user id : ', user_id)
            freq_image = {'top' : [], 'bottom' : [], 'outer' : [], 'dress' : []}
            media_url = '13.124.208.47:8000/media/'

            category = request.POST.get('category', '')

            items = CATEGORY.items()

            category_items = [x[0] for x in items if x[1] == category]

            result = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__category__in=category_items).values('clothes__image')

            clothes_url = [media_url + x['clothes__image'] for x in result]

            return JsonResponse({'msg' : 'frequency result', 'clothes_url' : clothes_url}, status=200)
        except Exception as e : 
            print('Frequency e : ', e)
            return JsonResponse({'msg' : e}, status = 400)
