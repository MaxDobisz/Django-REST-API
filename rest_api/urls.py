from django.urls import path
from . import views

urlpatterns = [
    path('persons/', views.persons),
    path('persons/<int:person_id>', views.persons, name="persons"),
    path('persons/filter/', views.persons_filter, name="persons-filter")
]