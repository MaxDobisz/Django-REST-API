from rest_framework.test import APITestCase
from rest_api.models import Person
from rest_api.serializer import PersonSerializer
import base64

class BasicTestsSetUp(APITestCase):
    def setUp(self):
        self.admin = Person.objects.create(
            first_name="admin",
            last_name="admin",
            email="admin@email.com",
            phone="07555555555",
            date_of_birth="2000-01-01",
            age=23,
            username="admin",
            password="admin"
        )

        self.quest = Person.objects.create(
            first_name="Ford",
            last_name="Focus",
            email="ford@email.com",
            phone="07512345678",
            date_of_birth="2000-01-01",
            age=23,
            username="quest1",
            password="12345"
        )

class PersonsViewTests(BasicTestsSetUp):
    def setUp(self):
        super().setUp()
        credentials = base64.b64encode(b'admin:admin').decode('utf-8')
        self.auth_header = f'Basic {credentials}'
        
    def test_create_person(self):
        url = '/persons/'
        data = {
            "first_name": "Nick",
            "last_name": "Carraway",
            "email": "nick@email.com",
            "phone": "07598765430",
            "date_of_birth": "1925-01-01",
            "age": 98,
            "username": "nick",
            "password": "12345"
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'Nick', 201)
    
    def test_get_persons(self):
        url = '/persons/?limit=10&offset=0'
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['results'])

    def test_get_single_person(self):
        url = '/persons/1'
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)

    def test_put_person(self):
        url = '/persons/2'
        data = {
            "first_name": "Barry",
            "last_name": "White",
            "email": "barry@email.com",
            "phone": "07598765430",
            "date_of_birth": "1999-01-01",
            "age": 24,
            "username": "Barry",
            "password": "12345"
        }
        
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(id=2)
        serialized_person = PersonSerializer(person)
        self.assertEqual(serialized_person.data['id'], 2)

    def test_patch_person(self):
        url = '/persons/2'
        data = {
            "first_name": "Harry",
            "username": "Harry",
        }
        
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(id=2)
        serialized_person = PersonSerializer(person)
        self.assertEqual(serialized_person.data['id'], 2)

    def test_delete_person(self):
        url = '/persons/2'
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 204)
        persons = Person.objects.count()
        self.assertEqual(persons, 1)

    def test_unauthenticated_access(self):
        url = '/persons/2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"ERROR": "Authentication credentials not provided."})

    def test_unauthorized_access(self):
        url = '/persons/2'
        credentials = base64.b64encode(b'guest:guest').decode('utf-8')
        auth_header = f'Basic {credentials}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"ERROR": "Invalid credentials."})

class PersonsFilterViewTests(BasicTestsSetUp):
    def test_filter_by_first_name(self):
        url = '/persons/filter/?first_name=ford'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Ford')

    def test_filter_by_partial_first_name(self):
        url = '/persons/filter/?first_name=fo'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Ford')
    
    def test_filter_by_last_name(self):
        url = '/persons/filter/?last_name=focus'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['last_name'], 'Focus')
    
    def test_filter_by_partial_last_name(self):
        url = '/persons/filter/?last_name=cus'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['last_name'], 'Focus')
    
    def test_filter_by_age(self):
        url = '/persons/filter/?age=23'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['age'], 23)

    def test_filter_by_first_name_and_last_name(self):
        url = '/persons/filter/?first_name=ford&last_name=focus'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Ford')
        self.assertEqual(response.data[0]['last_name'], 'Focus')

    def test_filter_by_last_name_and_age(self):
        url = '/persons/filter/?last_name=focus&age=23'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['last_name'], 'Focus')
        self.assertEqual(response.data[0]['age'], 23)

    def test_filter_by_first_name_last_name_and_age(self):
        url = '/persons/filter/?first_name=ford&last_name=focus&age=23'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'Ford')
        self.assertEqual(response.data[0]['last_name'], 'Focus')
        self.assertEqual(response.data[0]['age'], 23)

    def test_filter_by_invalid_first_name(self):
        url = '/persons/filter/?first_name=Greg'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_filter_without_any_parameters(self):
        url = '/persons/filter/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_invalid_age(self):
        url = '/persons/filter/?age=222222'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)