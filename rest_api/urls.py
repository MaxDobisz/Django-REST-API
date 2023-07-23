from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get-all', views.get_all)
]
