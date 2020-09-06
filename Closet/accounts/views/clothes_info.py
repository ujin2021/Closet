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

class ClothesInfo(ListView):
    def get(self, request):
        try :
            queryset = Clothes_category.objects.all()
            serializer = ClothesInfoSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e :
            print('ClothesInfo get e : ', e)
            return JsonResponse(e, safe=False)

    @LoginConfirm
    def post(self,request):
        try : 
            user_id = request.user.id
            print("request user id: ", user_id)
            
            classify = request.POST.get('classify', '') # color_pattern_category(_IN/OUT)
            print('classify : ', classify)
            class_arr = classify.split('_') # 처음등록시 len=3, IN/OUT update시 len=4

            color = class_arr[0]
            pattern = class_arr[1]
            category = class_arr[2]

            if(len(class_arr) == 3): # 처음 등록
                image = request.FILES.get('image') # image file name
                nowDate = now.strftime('%Y/%m/%d') # for media dir path
                image_path = nowDate+'/'+str(image) # image 저장 경로가 yy/mm/dd/[image_name]
                print('image name from app: ', image, 'image path: ', image_path) 
                
                form = Clothes_category(image=image, color=color, pattern=pattern, category=category)
                form.save() # clothes_category db에 clothes info 저장
                print("save complete")
            
                clothes = Clothes_category.objects.get(image=image_path) # 방금 저장한 옷의 row 가져오기
                print("clothes row id : ", clothes.id) # 해당 옷의 id
                closet_form = User_Closet(user_id=request.user.id, clothes_id=clothes.id) # user_closet db에 (user id, clothes id) 저장
                closet_form.save()

                return JsonResponse({'msg': 'save ok'}, status=201)

            if(len(class_arr) == 4): # IN/OUT update
                clothes = Clothes_category.objects.filter(color=color, pattern=pattern, category=category) # 옷장 camera가 옷을 분석한 결과와 일치하는 옷 찾기
                print('clothes id : ', clothes, ' leng : ', len(clothes))
                clothes_list = list(map(lambda x : x.id, clothes)) # clothes_category 에서 분류와 일치하는 옷의 id list
                print(clothes_list)
                
                for i in clothes_list:
                    result = User_Closet.objects.select_related('clothes').filter(clothes_id=i, user_id=user_id) # 옷이 해당 user의 것인지 확인
                    if(len(result) > 0): # 해당 user의 옷
                        print('result[0] : ', result[0])
                        break

                print('result id: ', result[0].id) # user_closet 의 id
                print('clothes id : ', result[0].clothes_id)

                status = class_arr[3]
                print('status : ', status)
                
                clothes = Clothes_category.objects.get(id = result[0].clothes_id) # 해당 옷 status update위해 obj 가져옴
                
                sid = transaction.savepoint()

                if(status == 'IN'):
                    clothes.status = True
                else:
                    clothes.status = False
                clothes.save() # savepoint 1

                # IN/OUT 시 user_closet의 frequency +1 -> transaction code
                user_closet_obj = result[0]
                frequency = user_closet_obj.frequency + 1
                user_closet_obj.frequency = frequency
                user_closet_obj.save() # savepoint 2

                transaction.savepoint_commit(sid)

                return JsonResponse({'msg': 'status update ok'}, status=200)

        except Exception as e :
            print('clothesInfo e : ', e)
            transaction.savepoint_rollback(sid)
            return JsonResponse({'msg': e}, status=400)