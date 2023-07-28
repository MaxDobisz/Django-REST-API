from rest_framework.serializers import ModelSerializer
from .models import Person

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class FilteredPersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'dateOfBirth', 'age')



# "id": 6,
#             "first_name": "Leo",
#             "last_name": "Ackermann",
#             "email": "leo@email.com",
#             "phone": "07589754605",
#             "dateOfBirth": "1988-07-28",
#             "age": 35,
#             "username": "LE",
#             "password": "123"