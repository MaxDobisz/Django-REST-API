from rest_framework.serializers import ModelSerializer
from .models import Person

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class FilteredPersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'age')