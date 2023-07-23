from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer

@api_view(['GET'])
def index(request):
    return Response({"Abc":"get view"})

@api_view(['GET'])
def get_all(request):
    all_persons = Person.objects.all()
    serializer = PersonSerializer(all_persons, many=True)
    return Response(serializer.data)


