import unittest

from django.test import TestCase, Client
from unittest.mock import patch
from portal import tasks
from grab import Grab
from django.test import RequestFactory


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
        response = GRAB.go(self.portal['url_auth'])
        login = 'denisoed'
        password = 'gorod312'
        self.assertTrue(tasks.auth_portal(
            response, self.portal, login, password))

    def test_auth_portal_datanotfound(self):
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go(self.uncorrect_portal['url_auth'])
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

    def test_fill_fields(self):
        portal = {
            'inp_title': 'title',
            'inp_url': 'url',
            'inp_text': 'text',
        }
        input_data = {
            'title': 'New post',
            'url': 'https://google.com',
            'description': 'Best best best'
        }
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go('https://news.ycombinator.com/submit')
        self.assertEqual(
            tasks.fill_fields(response, portal, input_data), response)

    @patch('portal.tasks.fill_fields')
    @patch('portal.tasks.send')
    def test_send_spam(self, mock_fill_fields, mock_send):
        portals = [
            {
                'url_submit': 'https://news.ycombinator.com/submit',
            }
        ]
        input_data = {
            'title': 'New post',
            'url': 'https://google.com',
            'description': 'Best best best'
        }
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go('https://news.ycombinator.com/submit')
        mock_fill_fields.return_value = response
        mock_send.return_value = True
        self.assertTrue(tasks.send_spam(input_data, portals))

    def test_get_selected_logout_portal(self):
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
        self.assertEqual(tasks.get_selected_logout_portal(portal), portal[0])

    def test_get_selected_logout_portal_false(self):
        portal = [
            {
                'name': 'laBuda'
            }
        ]
        self.assertFalse(tasks.get_selected_logout_portal(portal))

    @patch('portal.tasks.get_login_page')
    def test_go_authenticate_true(self, mock_get_login_page):
        mock_get_login_page.return_value = True
        request_factory = RequestFactory()
        request = request_factory.get('/portal/create/', data=None)
        portal = {
            'name': 'Hacker news'
        }
        login = 'denisoed'
        password = 'gorod312'
        self.assertTrue(
            tasks.go_authenticate(request, portal, login, password))

    @patch('portal.tasks.get_login_page')
    def test_go_authenticate_false(self, mock_get_login_page):
        mock_get_login_page.return_value = False
        request_factory = RequestFactory()
        request = request_factory.get('/portal/create/', data=None)
        portal = {
            'name': 'Hacker news'
        }
        login = 'denisoed'
        password = 'gorod312'
        self.assertFalse(
            tasks.go_authenticate(request, portal, login, password))


if __name__ == '__main__':
    unittest.main()
