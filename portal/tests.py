from django.test import TestCase, Client
from .forms import *
from .models import *

client = Client()


class PortalTest(TestCase):
    def create_portal(self):
        portal_models = Portal.objects.create(name='name', user="user")
        return Portal.objects.create(name='name', user="user")
        self.assertEqual(portal_models.name, 'name')
        self.assertEqual(portal_models.user, 'user')

    def test_creation(self):
        w = self.create_portal()
        self.assertTrue(isinstance(w, Portal))
        self.assertEqual(w.__str__(), w.name)


class User_Form_Test(TestCase):
    def test_UserForm_valid(self):
        form = PortalForm(data={'name': "us", 'user': "user"})
        self.assertTrue(form.is_valid())
