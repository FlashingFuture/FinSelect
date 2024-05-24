from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    
    GENDER_CHOICES = [
        (MALE, '남성'),
        (FEMALE, '여성'),
        (OTHER, '기타'),
    ]
    
    age = models.IntegerField(verbose_name='나이')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='성별')
    