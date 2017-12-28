from django.test import TestCase, Client
from unittest.mock import patch
from django.test import RequestFactory
from portal.models import Portal
from main.views import catch_data


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.input_data = {
            'title': 'title',
            'url': 'http://grablib.org',
            'description': 'Autumn'
        }
        self.empty_data = {
            'title': '',
            'url': '',
            'description': ''
        }
        self.small_data = {
            'title': 't',
            'url': 'www',
            'description': 'df'
        }
        self.user_valid_data = {
            'login': 'denisoed',
            'password': 'gorod312'
        }

    def test_for_connection(self):
        responce = self.client.get('http://127.0.0.1:8000/main/')
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_empty_data(self):
        responce = self.client.post('/main/', self.empty_data)
        self.assertTemplateUsed('index.html')
        self.assertEqual(responce.status_code, 302)

    @patch('django.contrib.auth.get_user')
    def test_for_portal_create(self, mock_get_user):
        mock_get_user.return_value = 'gulya'
        request_factory = RequestFactory()
        data = {
            'title': 'title',
            'url': 'www.google.com',
            'description': 'description'
        }
        login = 'denisoed'
        print(login)
        password = 'gorod312'
        print(password)
        selected_portal = Portal.objects.create(name='Hacker News',
                                                user='gulya')
        print(selected_portal)
        request = request_factory.post('/main/',
                                       data=data)
        self.assertEqual(catch_data(request).status_code, 302)
