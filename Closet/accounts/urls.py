from django.urls import path
from .views import user, clothes_info, recommendation, mypage

urlpatterns = [
    path('signup/', user.signup), #회원가입
    path('login/', user.login), # 로그인
    path('kakao_login/', user.kakao_login), # kakao login
    path('google_login/', user.google_login), # google login
    path('activate/<str:uidb64>/<str:token>', user.Activate.as_view()), # email 인증
    path('email-verify/', user.email_verify),
    path('clothes_info/', clothes_info.ClothesInfo.as_view()), # 옷 정보 받기, IN/OUT check
    path('recommendation/', recommendation.ClothesRecommendation.as_view()), # 옷 추천 리스트
    path('mypage/', mypage.Mypage.as_view()), # my 정보들 보내준다
    # 옷 추천 해준 3세트 중 한세트를 선택했을 때 세트 정보 보내기
]