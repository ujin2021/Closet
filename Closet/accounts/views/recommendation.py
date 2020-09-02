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

# https://gist.github.com/ujin2021/94df639614dbecff24325787185481df -> 옷 category 
# select_related -> db성능 개선        
class Recommendation(ListView) :
    @LoginConfirm
    def post(self, request) : 
        try :
            user_id = request.user.id
            print('request user id : ', user_id)

            hashtag = request.POST.get('hashtag', '') # 이거는 보내고
            color = request.POST.get('color', '') # color+weather+빈도수 보내주기
            weather = int(request.POST.get('weather', ''))

            user_clothes = User_Closet.objects.select_related('clothes').filter(user_id=user_id) # 사용자의 옷 id를 모두가져옴
            print('user_clothes : ', user_clothes)
            user_clothes_list = list(map(lambda x : x.clothes_id, user_clothes))

            clothesCateId = []
            for i in user_clothes_list :
                result = Clothes_category.objects.filter(id=i, status=1, color=color)
                if(len(result) > 0) :
                    clothesCateId.append(result[0]) # 해당하는 clothes의 id를 append

            # list -> json or 날씨별로 db저장해놓기
            if(weather >= 27) :
                weather_clothes = LEVEL[7]
            elif (weather >= 23) :
                weather_clothes = LEVEL[6]
            elif (weather >= 20) : 
                weather_clothes = LEVEL[5]
            elif (weather >= 17) : 
                weather_clothes = LEVEL[4]
            elif (weather >= 10) : 
                weather_clothes = LEVEL[3]
            elif (weather >= 6) : 
                weather_clothes = LEVEL[2]
            else :
                weather_clothes = LEVEL[1]

            weather_filtering = []
            for i in clothesCateId :
                clothes_id = i.id
                category = i.category
                print('id : ', clothes_id, ', category : ', category)
                if(category in weather_clothes) :
                    userClothesId = User_Closet.objects.filter(clothes_id=clothes_id)
                    weather_filtering.append(f'{i.color}_{i.pattern}_{i.category}_{userClothesId[0].frequency}')

            return JsonResponse({'code' : 200, 'msg' : weather_filtering}, status = 200)
            
        except Exception as e : 
            print('Recommendation e : ', e)
            return JsonResponse({'code' : 400, 'msg' : e}, status = 400)