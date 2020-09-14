from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL, CATEGORY
from ..tokenCheck import *
from ..recommendation_algorithm import recommendation
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
            user_clothes_obj = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__status=1, 
            clothes__category__in=weather_clothes).values("frequency", "clothes__category", "clothes__color", "clothes__pattern", "clothes__id")
            print('user_clothes_obj', user_clothes_obj)
            for obj in user_clothes_obj :
                if (obj['clothes__color'] == color) :
                    filtering[CATEGORY[obj['clothes__category']]].append(f'{obj["clothes__color"]}_{obj["clothes__pattern"]}_{obj["clothes__category"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]].append(obj["frequency"])
                else :
                    filtering[CATEGORY[obj['clothes__category']]+'_df'].append(f'{obj["clothes__color"]}_{obj["clothes__pattern"]}_{obj["clothes__category"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]+'_df'].append(obj["frequency"])
            
            recom_result = recommendation(filtering, filtering_freq, sex, hashtag, weather) # 이것들을 찾아서 media url 전송해주기
            print('recom_result', recom_result)

            # android 에 media url 보내주고, 추천된 옷 
            clo_image = []
            for clo_set in recom_result :
                tmp = []
                for clo in clo_set :
                    clo_spl = clo.split('_')
                    clothes = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__status=1, 
                    clothes__color=clo_spl[0], clothes__pattern=clo_spl[1], clothes__category=clo_spl[2]).values("clothes__id", "clothes__image")
                    print('clothes image: ', clothes) # clothes image:  <QuerySet [{'clothes__id': 55, 'clothes__image': '2020/09/02/14.jpg'}]>
                    # tmp.append(clothes.)

            return JsonResponse({'msg' : 'ok'}, status = 200)
            # android 로 옷세트들({'top' : 'top_image_url', 'bottom' : 'bottom_image_url' ... })
            
        except Exception as e : 
            print('Recommendation e : ', e)
            return JsonResponse({'msg' : e}, status = 400)