import unittest

from django.test import TestCase, Client
from unittest.mock import patch
from portal import tasks


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

    @patch('portal.tasks.auth_portal')
    def test_get_login_page(self, mock_auth_portal):
        mock_auth_portal.return_value = True
        request = 'Fake'
        self.assertTrue(tasks.get_login_page(request, self.portal, None, None))

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


if __name__ == '__main__':
    unittest.main()
