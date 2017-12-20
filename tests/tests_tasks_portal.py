import unittest

from django.test import TestCase, Client
from unittest.mock import patch
from portal import tasks
from grab import Grab

GRAB = Grab()


class TestTasks(TestCase):

    def setUp(self):
        self.client = Client()
        self.portal = {
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
        self.uncorrect_portal = {
                'url_auth': 'https://google.com',
                'auth_by': '<form method="post" action="login">'
            }

    @patch('portal.tasks.auth_portal')
    def test_get_login_page(self, mock_auth_portal):
        mock_auth_portal.return_value = True
        self.assertTrue(tasks.get_login_page(self.portal, None, None))

    @patch('portal.tasks.auth_portal')
    def test_get_login_page_datanotfound(self, mock_auth_portal):
        mock_auth_portal.return_value = True
        self.assertTrue(tasks.get_login_page(
            self.uncorrect_portal, None, None))

    def test_auth_portal_true(self):
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go(
            self.portal['url_auth'],
            log_file='templates/grab/bug_auth_portal.html')
        login = 'denisoed'
        password = 'gorod312'
        self.assertTrue(tasks.auth_portal(
            response, self.portal, login, password))

    def test_auth_portal_datanotfound(self):
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go(
            self.uncorrect_portal['url_auth'],
            log_file='templates/grab/bug_auth_portal.html')
        login = 'denisoed'
        password = 'gorod312'
        error = "Вы уже аутентифицированы"
        self.assertEqual(tasks.auth_portal(
            response, self.portal, login, password), error)

    def test_get_selected_portal(self):
        portal = [
            {
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
        ]
        data = ['Hacker news']
        self.assertEqual(tasks.get_selected_portal(data), portal)


if __name__ == '__main__':
    unittest.main()
