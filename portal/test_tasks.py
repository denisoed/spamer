import requests

from django.test import TestCase, Client
from portal import tasks


class TestTasks(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_login_page(self):
        correct_login_page = 'https://news.ycombinator.com/login'
        responce = requests.get(correct_login_page)
        self.assertEqual(responce.status_code, 200)

    def test_incorrect_login_page(self):
        incorrect_login_page = 'https://news.ycombinator.com/lagen'
        responce = requests.get(incorrect_login_page)
        self.assertEqual(responce.status_code, 404)

    def test_get_registered_user(self):
        user = 'denisoed'
        get_user = 'https://news.ycombinator.com/user?id={}'.format(user)
        responce = requests.get(get_user)
        res_text = responce.text
        self.assertNotEqual(res_text.find(user), -1)

    def test_registered_user_not_found(self):
        user = 'silvester-stalone'
        get_user_url = 'https://news.ycombinator.com/user?id={}'.format(user)
        responce = requests.get(get_user_url)
        res_text = responce.text
        self.assertEqual(res_text.find(user), -1)

    def test_get_selected_portal(self):
        portal = [
            {
                'name': 'Hacker news',
                'url_auth': 'https://news.ycombinator.com/login',
                'url_submit': 'https://news.ycombinator.com/submit',
                'inp_login': 'acct',
                'inp_password': 'pw',
                'inp_title': 'title',
                'inp_url': 'url',
                'inp_text': 'text',
                'auth_by': '<form method="post" action="login">',
                'auth_complete': '<span class="pagetop">'
            }
        ]
        data = ['Hacker news']
        self.assertEqual(tasks.get_selected_portal(data), portal)

    def test_successful_auth_in_portal(self):
        login = 'denisoed'
        password = 'gorod312'
        response = requests.post('https://news.ycombinator.com/login',
                                 data={'acct': login, 'pw': password})
        res_text = response.text
        self.assertNotEqual(res_text.find('logout'), -1)

    def test_failed_auth_in_portal_incorrect_data(self):
        login = 'silvester-stalone'
        password = 'my-best-password'
        response = requests.post('https://news.ycombinator.com/login',
                                 data={'acct': login, 'pw': password})
        res_text = response.text
        self.assertEqual(res_text.find('logout'), -1)
