import json
import bcrypt
import jwt
from .models import *
from .serializers import *
from .my_settings import SECRET_KEY, EMAIL
from .token import account_activation_token
from .text import message
from .tokenCheck import *
from .social_login import *
from .rasp_sendToken import *

from django.views import View
from django.views.generic import ListView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text

from datetime import datetime
now = datetime.now()

def signup(request, format=None):
    if request.method == "GET":
        try :
            queryset = Account.objects.all()
            serializer = AccountSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e :
            print('signup get e : ', e)
            return JsonResponse(e, safe=False)

    if request.method == "POST": # email, username이 null일 때도 확인, email form이 맞는지 확인
        try:           
            email = request.POST.get('email', '')
            pw = request.POST.get('password', '')
            password = bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
            username = request.POST.get('username', '')
   
            print("email = " + email+" username = " + username)
            myuser = Account.objects.filter(email=email)

            if myuser: # 이미 등록된 email이라면 회원가입 불가
                print("duplicated email")
                return JsonResponse({'code':400, 'msg':'duplicated email'}, status=201)
            else : 
                user = Account.objects.create(
                    email = email,
                    password=password,
                    username=username,
                    is_active=False,
                    platform=0
                )

                current_site = get_current_site(request)
                domain = current_site.domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                mail_title = "ICE CLOSET 이메일 인증"
                message_data = message(domain, uidb64, token)
                mail_to = email
                email = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send()

                print("signup success and send email")
                return JsonResponse({'code':201, 'msg':'signup success'}, status=201)

        except KeyError:
            return JsonResponse({'code':400, 'msg':'INVALID KEY'}, status=201)
        except TypeError:
            return JsonResponse({"code":400, 'msg':'INVALID_TYPE'}, status=201)
        except ValidationError:
            return JsonResponse({'code':400, 'msg':'VALIDATION ERROR'}, status=201)
        except Exception as e:
            print('signup post e : ', e)
            return JsonResponse({'code':400, 'msg':e}, status=201)

def login(request, format=None): 
    try :
        if request.method == "POST":
            email = request.POST.get('email', '')
            print('login email = ' , email)
            myuser = Account.objects.filter(email=email)
            if myuser: # email이 db에 저장되어있으면
                print("email exits")
                user = Account.objects.get(email=email)
                password = request.POST.get('password', '')
                if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
                    print("password correct, my user!")
                    if user.is_active == True: # email 인증까지 완료한 회원이면 로그인 성공
                        print("user is_active turns True")
                        token = jwt.encode({'user':user.id}, SECRET_KEY['secret'], SECRET_KEY['algorithm']).decode('UTF-8')
                        print("token = ", token)
                        return JsonResponse({'code':201, 'msg':'login success', 'token':token}, status=201) # login 시 token 발급
                    return JsonResponse({'code':0, 'msg':'not activated account'}, status=201) # email 활성화 되지 않음
                return JsonResponse({'code':1, 'msg':'password incorrect'}, status=201) # email에 매칭된 pw가 틀림
            return JsonResponse({'code':2, 'msg':'not my user'}, status=201) # 해당 email이 db에 없음
    except Exception as e :
        print('login e : ', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)

def kakao_login(request, format=None): # 앱연동 테스트 해보기, get 넣어주기
    try :
        if request.method == "POST":
            platform = 1
            uid = request.POST.get('uid', '')
            email = request.POST.get('email', '')
            result = social_login(platform=platform, uid=uid, email=email) # social_login 파일에서 처리
            if(result == False): # uid or email 길이가 0 일 때
                return JsonResponse({'code':503, 'msg':'login fail', 'token':''}, status=201) # 소셜로그인 실패(정보가 안넘어왔을 경우)
            print("token : ", result['token'])
            return JsonResponse({'code':201, 'msg':'login success', 'token':result['token']}, status=201) # 소셜로그인 성공
    except Exception as e :
        print('kakao_login e :', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)

def google_login(request, format=None): # 앱연동 테스트 해보기, get 넣어주기
    try :
        if request.method == "POST":
            platform = 2
            uid = request.POST.get('uid', '')
            email = request.POST.get('email', '')
            result = social_login(platform=platform, uid=uid, email=email)
            if(result == False):
                return JsonResponse({'code':503, 'msg':'login fail', 'token':'token fail'}, status=201) # 소셜로그인 실패(정보가 안넘어왔을 경우)
            return JsonResponse({'code':201, 'msg':'login success', 'token':result['token']}, status=201) # 소셜로그인 성공
    except Exception as e :
        print('google_login e : ', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)


# logout 시에는 android 앱에서 토큰을 더이상 넘겨주지 않으면 됨.
class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
            print("uid = ", uid, " user = ", user)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])
            return JsonResponse({'code':401, 'msg':'auth fail'}, status=201)

        except ValidationError:
            return JsonResponse({'code':400, 'msg':'TYPE ERROR'}, status=201)
        except KeyError:
            print("class Activate key error")
            return JsonResponse({'code':400, 'msg':'KEY ERROR'}, status=201)

def email_verify(request):
    try :
        return render(request, 'accounts/verify.html')
    except Exception as e :
        print('email_verify e : ', e)
        return render(request, e)

# CLEAN CODE!!
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

                return JsonResponse({'code':201, 'msg': 'save ok'}, status=200)

            if(len(class_arr) == 4): # IN/OUT update
                clothes = Clothes_category.objects.filter(color=color, pattern=pattern, category=category) # 옷장 camera가 옷을 분석한 결과와 일치하는 옷 찾기
                print('clothes id : ', clothes, ' leng : ', len(clothes))
                clothes_list = list(map(lambda x : x.id, clothes)) # clothes_category 에서 분류와 일치하는 옷의 id list
                print(clothes_list)
                
                for i in clothes_list:
                    result = User_Closet.objects.filter(clothes_id=i, user_id=user_id) # 옷이 해당 user의 것인지 확인
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

                return JsonResponse({'code':201, 'msg': 'status update ok'}, status=200)

        except Exception as e :
            print('clothesInfo e : ', e)
            transaction.savepoint_rollback(sid)
            return JsonResponse({'code':400, 'msg': e}, status=400)


# https://gist.github.com/ujin2021/94df639614dbecff24325787185481df
class ClothesList(ListView):
    @LoginConfirm
    def post(self, request): # (token+(날씨?) -> 해당회원의 옷 보내줌) (토큰+그중에 하나고름 -> 하나고른것+날씨고려해서 머신러닝으로)
        try:
            user_id = request.user.id
            print("request user id: ", user_id)

            weather = request.POST.get('weather', '')

            user_clothes = User_Closet.objects.filter(user_id=user_id) # 사용자의 옷 id를 모두가져옴
            user_clothes_list = list(map(lambda x : x.clothes_id, user_clothes)) # clothes_category 에서 분류와 일치하는 옷의 id list
            print("user_clothes_list : ", user_clothes_list) # user_closet 에서 해당 사용자의 옷들
            
            filtering = []
            # 날씨 별 long or short는 정해야함(습도, 비/눈 고려)
            if (int(weather) > 20) :
                print('weather : ', int(weather))
                for i in user_clothes_list :
                    print('i : ', i)
                    result = Clothes_category.objects.filter(id=i, status=1)
                    if(len(result) > 0) :
                        print('result : ', result[0])
                        print('result.category', result[0].category)
                        category = result[0].category
                        if(category.find('short') > -1 or category.find('sshort') > -1 or category.find('slong') > -1):
                            filtering.append(result[0])

            print('filtering : ', filtering)
            filtering_list = list(map(lambda x : x.id, filtering))
            return JsonResponse({'code':201, 'msg': filtering_list}, status=200)

        except Exception as e :
            print ('ClothesList e : ', e)
            return JsonResponse({'code' : 400, 'msg' : e}, status = 400)

