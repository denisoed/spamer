from django.test import TestCase, Client
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
        self.user1 = {
            'login': 'testuser',
            'password': 'qwerty123'
        }

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_login_user(self):
        response = self.client.post('/account/login/', self.user)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/account/login/',
                                       status_code=302, target_status_code=200)

    def test_if_user_is_not_None(self):
        response = self.client.post('/account/login/', self.user1)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('login.html')

    def test_logout_user(self):
        response = self.client.get('/account/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('login.html')

    def test_get_login_page(self):
        response = self.client.get('/account/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('login.html')
