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

@api_view(['GET'])
def get_person(request):
    person_id = request.data.get('person_id')
    try:
        person = Person.objects.get(id=person_id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    except Person.DoesNotExist:
        return Response({"ERROR":"The person dose not exist"}, status=404)

@api_view(['GET', 'POST'])
def create_person(request):
    data = request.data
    serializer = PersonSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"SUCCESS":"The person has been created" }, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['Delete'])
def delete_person(request):
    person_id = request.data.get('person_id')
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return Response({"SUCCESS":"The person has been deleted"})
    except Person.DoesNotExist:
        return Response({"ERROR":"The person dose not exist"}, status=404)
    
@api_view(['PUT'])
def update_person(request):
    person_id = request.data.get('person_id')
    get_new_first_name = request.data.get('new_first_name')
    get_new_last_name = request.data.get('new_last_name')
    get_new_email = request.data.get('new_email')
    get_new_phone = request.data.get('new_phone')
    get_new_dateOfBirth = request.data.get('new_dateOfBirth')
    get_new_age = request.data.get('new_age')
    get_new_username = request.data.get('new_username')
    get_new_password = request.data.get('new_password')

    try:
        person = Person.objects.get(id=person_id)

        if get_new_first_name:
            person.first_name = get_new_first_name
        if get_new_last_name:
            person.last_name = get_new_last_name
        if get_new_email:
            person.email = get_new_email
        if get_new_phone:
            person.phone = get_new_phone
        if get_new_dateOfBirth:
            person.dateOfBirth = get_new_dateOfBirth
        if get_new_age:
            person.age = get_new_age
        if get_new_username:
            person.username = get_new_username
        if get_new_password:
            person.password = get_new_password
        
        person.save()
        return Response({"SUCCESS":"The person has been updated"})
    
    except Person.DoesNotExist:
        return Response({"ERROR":"The person dose not exist"}, status=404)  