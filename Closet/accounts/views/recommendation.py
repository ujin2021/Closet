from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL, LEVEL, CATEGORY
from ..tokenCheck import *
from ..Recommendation_algo.recommendation_algorithm import Recommendation as Rd
from django.views.generic import ListView
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from datetime import datetime
now = datetime.now()

media_url = '13.124.208.47:8000/media/'

# https://gist.github.com/ujin2021/94df639614dbecff24325787185481df -> 옷 category 
# 클린코드, 리팩토링 하기      
class ClothesRecommendation(ListView) :
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

            recom_list = Recommendation.objects.select_related('clothes').filter(user_id=user_id).values('top_id', 'bottom_id', 'outer_id', 'outer2_id', 'dress_id', 'neat_id')
            delete = []
            for i in recom_list :
                top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id = i['top_id'], i['bottom_id'], i['outer_id'], i['outer2_id'], i['dress_id'], i['neat_id']
                clo_id = [top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id]
                tmp = []
                for j in clo_id :
                    if(j):
                        clo = Clothes_category.objects.filter(id=j)
                        tmp.append(f'{clo[0].color}_{clo[0].pattern}_{clo[0].category}')
                delete.append(tuple(tmp))
            # Rd 에 파라미터값 넣을 때 F대신 'sex' : sex 로 바꿔주기
            print({'filtering' : filtering, 'filtering_freq' : filtering_freq, 'sex' : sex, 'hashtag' : hashtag, 'weather' : weather, 'delete' : delete})
            result = Rd({'filtering' : filtering, 'filtering_freq' : filtering_freq, 'sex' : 'F', 'hashtag' : hashtag, 'weather' : weather, 'delete' : delete})
            result.result_similarity()
            recom_result = result.outfit() # result

            for i in range(3) : # tuple을 list로
                if(type(recom_result[i]) == type('string')):
                    tmp = []
                    tmp.append(recom_result[i])
                    recom_result[i] = tmp
                else:
                    recom_result[i] = list(recom_result[i])
            print('recom_result', recom_result)

            # android 에 media url 보내주고, 추천된 옷 db에 저장하기 
            clo_image = {}
            for set_idx in range(len(recom_result)) :
                top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id = '', '', '', '', '', ''
                tmp = []
                for clo in recom_result[set_idx] :
                    clo_spl = clo.split('_')
                    clothes = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__status=1, 
                    clothes__color=clo_spl[0], clothes__pattern=clo_spl[1], clothes__category=clo_spl[2]).values("clothes__id", "clothes__image")
                    tmp.append(media_url + clothes[0]['clothes__image'])
                    
                    cate = CATEGORY[clo_spl[2]] # top, bottom, dress, outer
                    if(cate == 'top') : 
                        top_id = clothes[0]['clothes__id']
                    elif(cate == 'bottom') : 
                        bottom_id = clothes[0]['clothes__id']
                    elif(cate == 'outer') :
                        if('neatvest' in clo_spl[2]) :
                            neat_id = clothes[0]['clothes__id']
                        else:
                            if(len(str(outer_id)) == 0):
                                outer_id = clothes[0]['clothes__id']
                            else:
                                outer2_id = clothes[0]['clothes__id']
                    elif(cate == 'dress') :
                        dress_id = clothes[0]['clothes__id']

                if(set_idx == 0) :
                    key = 'first'
                elif(set_idx == 1) :
                    key = 'second'
                elif(set_idx == 2) :
                    key = 'third'
                clo_image[key] = tmp
                form = Recommendation(user_id=user_id, top_id=top_id, bottom_id=bottom_id, outer_id=outer_id, outer2_id=outer2_id, dress_id=dress_id, neat_id=neat_id)
                form.save()
            print('clo_image : ', clo_image)

            return JsonResponse({'msg' : 'recommend result', 'media_url' : clo_image}, status = 200)
            # return JsonResponse({'msg' : 'recommend result', 'media_url' : 'clo_image'}, status = 200)
            
        except Exception as e : 
            print('Recommendation e : ', e)
            return JsonResponse({'msg' : e}, status = 400)