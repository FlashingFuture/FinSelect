from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.conf import settings

UserModel = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
   MALE = 'M'
   FEMALE = 'F'
   OTHER = 'O'
    
   GENDER_CHOICES = [
        (MALE, '남성'),
        (FEMALE, '여성'),
        (OTHER, '기타'),
    ]
   
   age = serializers.IntegerField()
   gender = serializers.ChoiceField(choices=GENDER_CHOICES)
   email = serializers.EmailField()
   
   def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'age': self.validated_data.get('age', ''),
            'gender': self.validated_data.get('gender', ''),
        }
   
class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    @staticmethod
    def validate_username(username):
        if 'allauth.account' not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username
        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)

        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'gender'):
            extra_fields.append('gender') 
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')       
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)
