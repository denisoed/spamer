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
                'auth_by': '<form method="post" action="login">',
                'inp_login': 'acct',
                'inp_password': 'pw',
            }

    @patch('portal.tasks.get_selected_portal')
    @patch('portal.tasks.send', return_value=200)
    def test_send_spam(self, mock_get_selected_portal, mock_send):
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
        mock_get_selected_portal.return_value = portal
        port_list = ['Hacker news']
        correct_data = {
            'login': 'denisoed',
            'password': 'gorod312',
            'title': 'Title',
            'url': 'https://google.com',
            'description': 'bla bla bla'
        }
        self.assertTrue(tasks.send_spam(correct_data, port_list))

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

    def test_send(self):
        GRAB.go('https://google.com')
        self.assertEqual(tasks.send(GRAB).code, 200)


if __name__ == '__main__':
    unittest.main()
