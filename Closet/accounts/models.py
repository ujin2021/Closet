from django.db import models

# app user info
class Account(models.Model):
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
        ('N', 'None')
    )
    email = models.EmailField(max_length=100, unique=True) # email 겸 id
    password = models.CharField(max_length=200, null=True) # social login 시 uid
    username = models.CharField(max_length=100) # social login 시 @ 앞부분
    platform = models.IntegerField(default=0) # normal : 0, kakao : 1, google : 2
    is_active = models.BooleanField(default=False) # social login 시 무조건 1
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'account'

class RaspberryPi(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=50, unique=True)
    port = models.CharField(max_length=10)

    class Meta:
        db_table = 'raspberry_pi'

# user가 등록하는 옷들
class Clothes_category(models.Model):
    image = models.ImageField(upload_to="%Y/%m/%d", default=False, max_length=255)
    color = models.CharField(max_length=15, default='none')
    pattern = models.CharField(max_length=20, default='none')
    category = models.CharField(max_length=20, default='none')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'clothes_category'

# user + user의 clothes
class User_Closet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes_category, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_closet'


# 머신러닝에서 추천해준 옷 세트 리스트들(이것들은 일주일 안에 다시 추천해주면 안됨)
# http://xe.issro.net/MySQL/299 date 빼기 관련(일주일 지나면 삭제)
# https://brunch.co.kr/@ddangdol/4
class Recommendation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    top = models.ForeignKey(Clothes_category, related_name='rec_top', on_delete=models.CASCADE, null=True)
    bottom = models.ForeignKey(Clothes_category, related_name='rec_bottom',on_delete=models.CASCADE, null=True)
    outer = models.ForeignKey(Clothes_category, related_name='rec_outer',on_delete=models.CASCADE, null=True)
    outer2 = models.ForeignKey(Clothes_category, related_name='rec_outer2',on_delete=models.CASCADE, null=True)
    neat = models.ForeignKey(Clothes_category, related_name='rec_neat',on_delete=models.CASCADE, null=True)
    dress = models.ForeignKey(Clothes_category, related_name='rec_dress', on_delete=models.CASCADE, default=True, null=True)
    recommend_at = models.DateField(auto_now=True) # insert 될때, status 바뀔때(추천금지->추천가능) 자동으로 date update 되도록

    class Meta:
        db_table = 'recommendation'

# 추천리스트 중 사용자가 입은 옷 세트
class Frequency_Fashion(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    top = models.ForeignKey(Clothes_category, related_name='fre_top', on_delete=models.CASCADE, null=True)
    bottom = models.ForeignKey(Clothes_category, related_name='fre_bottom', on_delete=models.CASCADE, null=True)
    outer = models.ForeignKey(Clothes_category, related_name='fre_outer', on_delete=models.CASCADE, null=True)
    outer2 = models.ForeignKey(Clothes_category, related_name='fre_outer2',on_delete=models.CASCADE, null=True)
    neat = models.ForeignKey(Clothes_category, related_name='fre_neat',on_delete=models.CASCADE, null=True)
    dress = models.ForeignKey(Clothes_category, related_name='fre_dress', on_delete=models.CASCADE, default=True, null=True)

    class Meta:
        db_table = 'frequency_fashion'