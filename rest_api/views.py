
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer, FilteredPersonSerializer
from rest_framework.pagination import LimitOffsetPagination
import base64

@api_view(['GET', 'POST', 'PUT', 'PATCH','DELETE'])
@authentication_classes([])
@permission_classes([])
def persons(request, person_id=None):
    header_auth = request.META.get('HTTP_AUTHORIZATION')

    if header_auth and header_auth.startswith('Basic'):
        credentials = header_auth[6:].strip()
        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        user_name, password = decoded_credentials.split(':', 1)
        if user_name == 'admin':
            try:
                admin = Person.objects.get(username='admin')
                if admin.password == password:
                    if request.method == 'GET':
                        if person_id:
                            try:
                                person = Person.objects.get(id=person_id)
                                serializer = PersonSerializer(person)
                                return Response(serializer.data, status=200)
                            except Person.DoesNotExist:
                                return Response({"ERROR":"The person dose not exist"}, status=404)
                        else:
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
                    elif request.method == 'POST':
                        data = request.data
                        serializer = PersonSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({"SUCCESS":"The person has been created" }, status=201)
                        else:
                            return Response(serializer.errors, status=400)
                    elif request.method == 'PUT':
                        if person_id:
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
                                return Response({"SUCCESS": "The person has been updated"}, status=200)
                            except Person.DoesNotExist:
                                return Response({"ERROR": "The person does not exist"}, status=404) 
                        else:
                            return Response({"ERROR": "The person id not provided"}, status=404) 
                    elif request.method == 'PATCH':
                        try:
                            person = Person.objects.get(id=person_id)
                            for field in request.data:
                                if field in person.__dict__:
                                    setattr(person, field, request.data[field])
                            person.save()
                            return Response({"SUCCESS": "The person has been updated"}, status=200)
                        except Person.DoesNotExist:
                            return Response({"ERROR": "The person does not exist"}, status=404) 
                    elif request.method == 'DELETE':
                        try:
                            person = Person.objects.get(id=person_id)
                            person.delete()
                            return Response({"SUCCESS":"The person has been deleted"}, status=204)
                        except Person.DoesNotExist:
                            return Response({"ERROR":"The person dose not exist"}, status=404)
                else:
                    return Response({"ERROR": "Invalid credentials."}, status=401)
                
            except Person.DoesNotExist:
                            return Response({"ERROR": "The admin does not exist"}, status=404)    
        else:
            return Response({"ERROR": "Invalid credentials."}, status=401)   
    else:
        return Response({"ERROR": "Authentication credentials not provided."}, status=401)

@api_view(['GET'])
def persons_filter(request):
    queryset = Person.objects.all()
    first_name = request.query_params.get('first_name', None)
    last_name = request.query_params.get('last_name', None)
    age = request.query_params.get('age', None)

    if first_name:
        queryset = queryset.filter(first_name__icontains=first_name)
    if last_name:
        queryset = queryset.filter(last_name__icontains=last_name)
    if age:
        queryset = queryset.filter(age=age)

    serializer = FilteredPersonSerializer(queryset, many=True)

    return Response(serializer.data, status=200)