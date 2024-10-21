from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from notes import serializers
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note


class UserRoutesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        User.objects.create_superuser(username='lucas', email='admin@admin.com', password='admin')
        User.objects.create(username="user1", email="test1@test.com", password="test")
        User.objects.create(username="user2", email="test2@test.com", password="test2")

    def test_get_all_users_as_admin(self):   # GET users/
        self.api_client.login(username='lucas', password='admin')
        response = self.api_client.get(reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(), 3)
        self.api_client.logout()
    
    def test_get_all_users_not_admin(self):
        self.api_client.login(username='user1', password='test')
        response = self.api_client.get(reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.api_client.logout()

    def test_get_one_user_as_admin(self):    # GET users/<int:pk>
        self.api_client.login(username='lucas', password='admin')
        user_1 = User.objects.get(username="user1")
        response = self.api_client.get(reverse('user-detail', kwargs={'pk': user_1.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_1.username, response.data['username'])
        self.api_client.logout()

    def test_create_user(self):         # POST register/
        response = self.api_client.post('/register/', data={'username': 'test_user', 'password': 'test', 'email': 'test@test.test'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 4)
        self.assertEqual(User.objects.filter(username='test_user').count(), 1)

    # TODO: Figure out changing credentials (+ implementing JWT authentication)
    # def test_update_own_password(self): # PUT users/<int:pk>
    #     self.fail()

    # def test_update_own_email(self):    # PUT users/<int:pk>
    #     self.fail()

    # def test_update_own_username(self): # PUT users/<int:pk>
    #     self.fail()


class NoteRoutesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        User.objects.create_superuser(username='lucas', email='admin@admin.com', password='admin')
        User.objects.create(username="user1", email="test1@test.com", password="test")
    
    def setUp(self):
        self.api_client.force_authenticate(user=User.objects.get(username='lucas'))
        self.api_client.post('/notes/', data={'title': 'test note', 'note': 'this is a test'})

        self.api_client.force_authenticate(user=User.objects.get(username='user1'))
        self.api_client.post('/notes/', data={'title': 'note deux', 'note': 'nooooootes'})
        self.api_client.post('/notes/', data={'title': 'note trois', 'note': 'this is a third note'})

        self.api_client.force_authenticate(user=None)
    
    def test_get_own_note(self):
        self.api_client.login(username="lucas", password="admin")
        note = Note.objects.filter(title='test note').first()

        response = self.api_client.get(f"/notes/{note.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.api_client.logout()

    def test_get_someone_elses_note(self):
        self.api_client.login(username="user1", password="test")
        note = Note.objects.filter(title='test note').first()

        response = self.api_client.get(f"/notes/{note.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.api_client.logout()

    def test_get_my_notes(self):
        self.api_client.force_authenticate(user=User.objects.get(username='user1'))
        response = self.api_client.get('/my-notes/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.api_client.force_authenticate(user=None)

    def test_delete_note(self):
        self.api_client.force_authenticate(user=User.objects.get(username='user1'))
        note = Note.objects.get(title='note trois')
        response = self.api_client.delete(f"/notes/{note.pk}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.api_client.get('/my-notes/')
        self.assertEqual(len(response.data), 1)

        self.api_client.force_authenticate(user=None)

    def test_update_title(self):
        self.api_client.force_authenticate(user=User.objects.get(username='user1'))
        note = Note.objects.get(note='this is a third note')

        response = self.api_client.put(f"/notes/{note.pk}/", data={'title': 'test title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        note = Note.objects.get(note='this is a third note')
        self.assertEqual(note.title, 'test title')

        self.api_client.force_authenticate(user=None)

    def test_update_note(self):
        self.api_client.force_authenticate(user=User.objects.get(username='user1'))
        note = Note.objects.get(title='note trois')

        response = self.api_client.put(f"/notes/{note.pk}/", data={'note': 'we changed the text'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        note = Note.objects.get(title='note trois')
        self.assertEqual(note.note, 'we changed the text')

        self.api_client.force_authenticate(user=None)