from django.test import TestCase, Client
from .factories import UserAuthFactory
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from importlib import import_module
from django.conf import settings


class TestAuth(TestCase):

    def setUp(self):
        self.client = Client()
        self.data = {
            'username': 'testuser',
            'password1': 'qwerty123',
            'password2': 'qwerty123'
        }
        self.user = {
            'username': 'testuser',
            'password': 'qwerty123'
        }

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_register_user(self):
        response = self.client.post('/account/register/', self.data)    
        self.assertEquals(response.status_code, 302)

    def test_login_user(self):
        user = self.client.post('/account/register/', self.data)
        response = self.client.post('/account/login/', self.user)
        # login = self.client.login(username=self.user['username'], password=self.user['password'])
        # auth_user = auth.authenticate(username=self.user['username'], password=self.user['password'])
        # a = auth.login(self.client.request, auth_user)
        # self.assertTrue(a)
        # self.assertTrue(auth_user.is_authenticated)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('main.html')

    def test_logout_user(self):
        response = self.client.get('/account/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('login.html')

    def test_get_register_page(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)

    def test_get_login_page(self):
        response = self.client.get('/account/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('login.html')
