from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Thesis, CustomUser, DefenseCouncil, ThesisScore

from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'role', 'major', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = CustomUser(**data)
        user.set_password(data['password'])
        user.save()

        return user


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Mật khẩu mới và xác nhận mật khẩu không khớp")

        return data


class DefenseCouncilSerializer(ModelSerializer):
    class Meta:
        model = DefenseCouncil
        fields = '__all__'


class ThesisSerializer(ModelSerializer):
    class Meta:
        model = Thesis
        fields = '__all__'


class ThesisScoreSerializer(ModelSerializer):
    class Meta:
        model = ThesisScore
        fields = '__all__'
