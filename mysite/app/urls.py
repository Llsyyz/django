from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("index/", views.index, name="index"),
    path("index/deal", views.deal, name="deal"),
]