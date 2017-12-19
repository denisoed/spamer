from django.test import TestCase, Client
from django.urls import reverse
from portal.forms import PortalForm
from portal.models import Portal
from portal.views import find_selected_portal


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
        print(name_obj)
        self.assertEqual(name_obj, data)

    def test_for_delete_portals(self):

        data = {'login': 'login', 'password': '2323232'}
        r = self.client.post(reverse('portal:delete_portal',
                                     kwargs={'id_portal': 1}), data=data)
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, '/main/',
                             status_code=302, target_status_code=200)
