from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
import jwt
from .userManage import UserManager
from datetime import datetime,timedelta

class User(AbstractBaseUser):
    id=models.AutoField(primary_key=True,null=False)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=60)
    password=models.CharField(max_length=16)
    username=models.CharField(max_length=20,unique=True)
    mobileNumber=models.IntegerField()

    USERNAME_FIELD = 'username'
    objects=UserManager()

class Movie(models.Model):
    movie_id=models.AutoField(primary_key=True,null=False)
    theatres=models.ManyToManyField("Theatre", related_name="movies")
    name=models.CharField(max_length=50)
    image=models.CharField(max_length=300)
    rating=models.FloatField()

class MovieDetail(models.Model):
    movie_id=models.IntegerField()
    language=models.CharField(max_length=50)
    genre=models.CharField(max_length=100)

class Theatre(models.Model):
    theatre_id=models.AutoField(primary_key=True,null=False)
    theatre_name=models.CharField(max_length=50)
    city=models.CharField(max_length=20,null=False)

class MovieTiming(models.Model):
    id_timing=models.AutoField(primary_key=True,null=False)
    movie_id=models.IntegerField()
    theatre_id=models.IntegerField()
    timing=models.DateTimeField(auto_now_add=True)
    bookedSeats=models.CharField(max_length=3000)

class Seat(models.Model):
    seat_id=models.AutoField(primary_key=True,null=False)
    seat_no=models.CharField(max_length=5)   
