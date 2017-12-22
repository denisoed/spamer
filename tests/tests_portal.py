from django.test import TestCase, Client
from django.urls import reverse
from portal.forms import PortalForm
from portal.models import Portal
from portal.views import find_selected_portal
from unittest.mock import patch
from portal.views import create_new_portal
from django.test import RequestFactory


client = Client()


class PortalTest(TestCase):

    def test_for_create_portal(self):
        portal_models = Portal.objects.create(name='Hacker News', user="user1")
        self.assertEqual(portal_models.name, 'Hacker News')
        self.assertEqual(portal_models.user, 'user1')
        assert isinstance(portal_models, Portal)


class TestForm(TestCase):

    def test_user_form_is_valid(self):
        data = {'name': "Hacker News", 'user': "admin",
                'login': 'hjhk', 'password': 'dfdfd'}
        form = PortalForm(data=data)
        self.assertTrue(form.is_valid(), True)

    def test_user_form__is_not_valid(self):
        form = PortalForm(data={'name': "Hacker News", 'user': "admin"})
        self.assertFalse(form.is_valid(), False)


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.userValidData = {
            'login': 'login',
            'password': 'pas'

        }
        self.validData = {
            'name': 'Hacker News',
            'user': 'user1'
        }
        self.data = {
            'name': 'Hacker news',
            'portals': 'Hacker news'
        }

    def test_for_connection(self):
        response = self.client.get('https://127.0.0.1:8000/portal/create/')
        self.assertTemplateUsed('index.html')
        self.assertRedirects(response, '/main/',
                             status_code=302, target_status_code=200)

    def test_if_portal_exists(self):
        data = {'name': "Hacker News", 'user': "admin",
                'login': 'user', 'password': '12345678'}
        portal_models = Portal.objects.create(name='Hacker News',
                                              user="user1")
        print(portal_models)
        r = self.client.post(reverse('portal:create_portal'), data=data)
        self.assertEqual(r.status_code, 302)

    def test_form_is_not_valid(self):
        data = {'name': "Hacker News", 'user': "admin"}
        r = self.client.post(reverse('portal:create_portal'), data=data)
        self.assertEqual(r.status_code, 302)

    def test_for_find_selected_portal(self):
        data = 'Hacker news'
        name_obj = find_selected_portal(data)['name']
        self.assertEqual(name_obj, data)

    def test_for_delete_portals(self):

        data = {'login': 'login', 'password': '2323232'}
        r = self.client.post(reverse('portal:delete_portal',
                                     kwargs={'id_portal': 1}), data=data)
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, '/main/',
                             status_code=302, target_status_code=200)

    @patch('portal.tasks.go_authenticate')
    def test_for_create_portal_error(self, mock_go_authenticate):
        mock_go_authenticate.return_value = False
        request_factory = RequestFactory()
        request = request_factory.get('/portal/create/', data=None)
        obj_portal = {
            'name': 'Hacker news',
            'url_auth': 'https://news.ycombinator.com/login',
            'url_logout': 'https://news.ycombinator.com/',
            'url_submit': 'https://news.ycombinator.com/submit',
            'inp_login': 'acct',
            'inp_password': 'pw',
            'inp_title': 'title',
            'inp_url': 'url',
            'inp_text': 'text',
            'auth_by': '<form method="post" action="login">',
            'auth_complete': '<span class="pagetop">'
        }
        login = 'denisoed'
        password = 'gorod312'
        selected_portal = Portal.objects.create(name='Hacker News',
                                                user="user1")
        self.assertEqual(create_new_portal(request, obj_portal,
                                           login, password,
                                           selected_portal).status_code, 302)

    @patch('django.contrib.auth.get_user')
    def test_for_portal_create(self, mock_get_user):
        mock_get_user.return_value = 'gulya'
        request_factory = RequestFactory()
        obj_portal = {
            'name': 'Hacker news',
            'url_auth': 'https://news.ycombinator.com/login',
            'url_logout': 'https://news.ycombinator.com/',
            'url_submit': 'https://news.ycombinator.com/submit',
            'inp_login': 'acct',
            'inp_password': 'pw',
            'inp_title': 'title',
            'inp_url': 'url',
            'inp_text': 'text',
            'auth_by': '<form method="post" action="login">',
            'auth_complete': '<span class="pagetop">'
        }
        login = 'denisoed'
        password = 'gorod312'
        selected_portal = Portal.objects.create(name='Hacker News',
                                                user='')
        request = request_factory.get(reverse('portal:create_portal'),
                                      data=None)
        self.assertEqual(create_new_portal(request, obj_portal, login,
                                           password,
                                           selected_portal).status_code, 302)
