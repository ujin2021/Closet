from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL, CATEGORY
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
            filtering = {'top' : [], 'bottom' : [], 'dress' : [], 'outer' : [], 'top_df' : [], 
            'bottom_df' : [], 'dress_df' : [], 'outer_df' : []}
            filtering_freq = {'top' : [], 'bottom' : [], 'dress' : [], 'outer' : [], 'top_df' : [], 
            'bottom_df' : [], 'dress_df' : [], 'outer_df' : []}

            user_id = request.user.id
            print('request user id : ', user_id)

            hashtag = request.POST.get('hashtag', '')
            color = request.POST.get('color', '') 
            weather = int(request.POST.get('weather', ''))
            sex = Account.objects.filter(id=user_id).values('sex')[0]['sex']

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

            # 사용자의 옷 obj을 모두가져옴
            user_clothes_obj = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__status=1, clothes__category__in=weather_clothes).values("frequency", "clothes__category", "clothes__color", "clothes__pattern")

            for obj in user_clothes_obj :
                if (obj['clothes__color'] == color) :
                    filtering[CATEGORY[obj['clothes__category']]].append(f'{obj["clothes__category"]}_{obj["clothes__color"]}_{obj["clothes__pattern"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]].append(obj["frequency"])
                else :
                    filtering[CATEGORY[obj['clothes__category']]+'_df'].append(f'{obj["clothes__category"]}_{obj["clothes__color"]}_{obj["clothes__pattern"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]+'_df'].append(obj["frequency"])
            
            print(f'filtering : {filtering}, filtering_freq : {filtering_freq}, sex : {sex}, hashtag : {hashtag}')

            return JsonResponse({'code' : 200, 'msg' : 'ok'}, status = 200)
            
        except Exception as e : 
            print('Recommendation e : ', e)
            return JsonResponse({'code' : 400, 'msg' : e}, status = 400)