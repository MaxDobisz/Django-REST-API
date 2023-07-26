from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('filtered-persons/', views.filtered_persons),
    path('get-person/', views.get_person),
    path('create-person/', views.create_person),
    path('delete-person/', views.delete_person),
    path('update-person/', views.update_person),
]