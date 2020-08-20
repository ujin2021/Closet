from rest_framework import serializers
from .models import *
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'username', 'platform', 'is_active']

class ClothesInfoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Clothes_category
        fields = ['image', 'color', 'category', 'pattern', 'status']