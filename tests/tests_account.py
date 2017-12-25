from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.test import RequestFactory
from account.views import authorization_user


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

    # def test_if_user_is_not_None(self):
    #     response = self.client.post(reverse('account:authorization user'), self.user1)
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed('login.html')

    def test_logout_user(self):
        response = self.client.get('/account/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('login.html')

    def test_get_register_page(self):
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post('/account/register/', self.data)
        self.assertEquals(response.status_code, 302)

    def test_get_login_page(self):
        response = self.client.get('/account/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('login.html')

    def test_login_user(self):
        self.client.post('/account/register/',
                         self.data)
        response = self.client.post('/account/login/',
                                    self.user)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/account/login/',
                             status_code=302, target_status_code=200)

    def test_form(self):
        data = {
            'username': '',
            'password1': 'qwerty123'
        }
        response = self.client.post('/account/register', data=data)
        self.assertEqual(response.status_code, 301)

    def test_for_invalid_form(self):
        data = {
            'username': '',
            'password': '',
            'password1': ''
        }
        response = self.client.post(reverse('account:register user'),
                                    data=data)
        self.assertEqual(response.status_code, 302)

    # @patch('django.contrib.auth.authenticate')
    # @patch('django.contrib.auth.login')
    # def test_for_authorization_user(self, mock_authenticate, mock_login):
    #     mock_authenticate.return_value = 'gulya'
    #     mock_login.return_value = None
    #     request_factory = RequestFactory()
    #     login = 'denisoed'
    #     password = 'gorod312'
    #     request = request_factory.post('/account/login/', data=None)
    #     self.assertEqual(authorization_user(request).status_code, 302)
