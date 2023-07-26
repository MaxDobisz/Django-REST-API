from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination


@api_view(['GET'])
def index(request):
    all_persons = Person.objects.all()
    pagination_class = LimitOffsetPagination()
    paginated_data = pagination_class.paginate_queryset(all_persons, request)
    serializer = PersonSerializer(paginated_data, many=True)
    response_data = {
        'count': all_persons.count(),
        'next': pagination_class.get_next_link(),
        'previous': pagination_class.get_previous_link(),
        'results': serializer.data
    } 
    
    return Response(response_data, status=200)

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
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_person(request):
    data = request.data
    serializer = PersonSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"SUCCESS":"The person has been created" }, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['Delete'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_person(request):
    person_id = request.data.get('person_id')
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return Response({"SUCCESS":"The person has been deleted"})
    except Person.DoesNotExist:
        return Response({"ERROR":"The person dose not exist"}, status=404)
    
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_person(request):
    person_id = request.data.get('person_id')

    try:
        person = Person.objects.get(id=person_id)

        fields_to_update = [
            'first_name', 'last_name', 'email', 'phone',
            'dateOfBirth', 'age', 'username', 'password'
        ]

        for field in fields_to_update:
            new_value = request.data.get('new_' + field)
            if new_value is not None:
                setattr(person, field, new_value)

        person.save()
        return Response({"SUCCESS": "The person has been updated"})
    
    except Person.DoesNotExist:
        return Response({"ERROR": "The person does not exist"}, status=404) 