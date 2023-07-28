from django.urls import path
from . import views

urlpatterns = [
    path('persons/', views.persons),
    path('persons/<int:person_id>/', views.persons, name="persons")
    # path('get-person/', views.get_person),
    # path('create-person/', views.create_person),
    # path('delete-person/', views.delete_person),
    # path('update-person/', views.update_person),
]