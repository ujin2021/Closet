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
            print(f'hashtag : {hashtag}, color : {color}, weather : {weather}, sex : {sex}')

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

            # 사용자의 옷 전체의 빈도수, 카테고리, 색, 패턴, 옷 id 가져옴
            user_clothes_obj = User_Closet.objects.select_related('clothes').filter(user_id=user_id, clothes__status=1, 
            clothes__category__in=weather_clothes).values("frequency", "clothes__category", "clothes__color", "clothes__pattern", "clothes__id")
            # print('user_clothes_obj', user_clothes_obj)
            # 모두 가져온 후에 선택한 색과 같으면 cate에, 다른색이면 _df에 넣는다. freq는 따로 넣는다.
            # CATEGORY 는 shortsleeve : top 형식 처럼 되어있음.
            for obj in user_clothes_obj :
                # print('obj : ', obj)
                if (obj['clothes__color'] == color) :
                    filtering[CATEGORY[obj['clothes__category']]].append(f'{obj["clothes__color"]}_{obj["clothes__pattern"]}_{obj["clothes__category"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]].append(obj["frequency"])
                else :
                    filtering[CATEGORY[obj['clothes__category']]+'_df'].append(f'{obj["clothes__color"]}_{obj["clothes__pattern"]}_{obj["clothes__category"]}')
                    filtering_freq[CATEGORY[obj['clothes__category']]+'_df'].append(obj["frequency"])

            # 추천했던 세트는 다시 추천하면 안된다. delete 에 넣어준다.
            recom_list = Recommendation.objects.select_related('clothes').filter(user_id=user_id).values('top_id', 'bottom_id', 'outer_id', 'outer2_id', 'dress_id', 'neat_id')
            delete = []
            for i in recom_list : # i 가 하나의 set
                top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id = i['top_id'], i['bottom_id'], i['outer_id'], i['outer2_id'], i['dress_id'], i['neat_id']
                clo_id = [top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id] # set 각각의 id
                tmp = []
                for j in clo_id :
                    if(j): # id 가 null 일수도 있다.
                        clo = Clothes_category.objects.filter(id=j)
                        tmp.append(f'{clo[0].color}_{clo[0].pattern}_{clo[0].category}')
                delete.append(tuple(tmp))
            
            print({'filtering' : filtering, 'filtering_freq' : filtering_freq, 'sex' : sex, 'hashtag' : hashtag, 'weather' : weather, 'delete' : delete})
            result = Rd({'filtering' : filtering, 'filtering_freq' : filtering_freq, 'sex' : sex, 'hashtag' : hashtag, 'weather' : weather, 'delete' : delete})
            result.result_similarity()
            recom_result = result.outfit() # result

            for i in range(len(recom_result)) : # result 가 tuple 이라 list로 바꿔준다.
                if(type(recom_result[i]) == type('string')): # dress같이 하나만 있으면 str이므로 따로 처리해준다.
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
                    tmp.append(media_url + clothes[0]['clothes__image']) # 각 옷의 img url 을 append
                    
                    # 각 옷의 category를 알아내서, recommendation 의 어느 컬럼(top_id, bottom_id, etc) 에 들어갈지 확인.
                    cate = CATEGORY[clo_spl[2]] # top, bottom, dress, outer
                    if(cate == 'top') : 
                        top_id = clothes[0]['clothes__id']
                    elif(cate == 'bottom') : 
                        bottom_id = clothes[0]['clothes__id']
                    elif(cate == 'outer') :
                        if('neatvest' in clo_spl[2]) :
                            neat_id = clothes[0]['clothes__id']
                        else:
                            if(len(str(outer_id)) == 0): # outer가 두개일 수 있어서
                                outer_id = clothes[0]['clothes__id']
                            else:
                                outer2_id = clothes[0]['clothes__id']
                    elif(cate == 'dress') :
                        dress_id = clothes[0]['clothes__id']

                # res를 보낼 때 key 값을 설정해주기 위해서
                if(set_idx == 0) :
                    key = 'first'
                elif(set_idx == 1) :
                    key = 'second'
                elif(set_idx == 2) :
                    key = 'third'

                clo_image[key] = tmp # 한 세트의 옷 img url을 clo_image 에 저장
                
                # 각옷의 category 를 찾아 추출한 id값을 넣어서 recommendation table에 저장
                form = Recommendation(user_id=user_id, top_id=top_id, bottom_id=bottom_id, outer_id=outer_id, outer2_id=outer2_id, dress_id=dress_id, neat_id=neat_id)
                form.save()

            print('clo_image : ', clo_image)
            return JsonResponse({'msg' : 'recommend result', 'media_url' : clo_image}, status = 200)
            
        except Exception as e : 
            print('Recommendation e : ', e)
            return JsonResponse({'msg' : e}, status = 400)

class SelectOne(ListView) :
    @LoginConfirm
    def post(self, request) : 
        try :
            select = request.POST.get('select', '') 
            print('select:', select)
            user_id = request.user.id
            print('request user id : ', user_id)

            img_list = select.split(',')

            for i in range(len(img_list)) :
                img_list[i] = img_list[i].replace(media_url, '')

            clothes_obj = Clothes_category.objects.filter(image__in=img_list).values('id', 'category')
            if(len(clothes_obj) != len(img_list)) :
                return JsonResponse({'msg' : 'clothes not exist'}, status = 400)
            print(clothes_obj)

            top_id, bottom_id, outer_id, outer2_id, dress_id, neat_id = '', '', '', '', '', ''
            for clothes in clothes_obj :
                clo_id = clothes['id']
                clo_cate = clothes['category']
                if(CATEGORY[clo_cate] == 'top') :
                    top_id = clo_id
                elif(CATEGORY[clo_cate] == 'bottom') :
                    bottom_id = clo_id
                elif(CATEGORY[clo_cate] == 'dress') :
                    dress_id = clo_id
                elif(CATEGORY[clo_cate] == 'outer') :
                    if('neatvest' in clo_cate) :
                            neat_id = clo_id
                    elif(len(outer_id) > 0) :
                        outer2_id = clo_id
                    else :
                        outer_id = clo_id
            result = Frequency_Fashion(user_id=user_id, top_id=top_id, bottom_id=bottom_id, outer_id=outer_id, outer2_id=outer2_id, dress_id=dress_id, neat_id=neat_id)
            result.save()
            return JsonResponse({'msg' : 'data store success'}, status = 200)
        except Exception as e :
            print('selectOne e : ', e)
            return JsonResponse({'msg' : e}, status = 400)