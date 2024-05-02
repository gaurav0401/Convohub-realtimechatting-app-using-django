from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path("", views.rooms , name="home"),
    path("logout" , views.logoutuser , name="logout"),
    path("loginuser" , views.loginUser , name="login"),
    path("signup" , views.handleSignUp, name="signup"),
    path("createroom" , views.createRoom, name="createroom"),
    path("deleteroom/<slug:slug>" , views.deleteRoom, name="deleteroom"),
    path("<str:slug>", views.room, name="room"),
  
]
