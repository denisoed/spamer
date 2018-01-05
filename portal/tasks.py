# -*- coding: utf-8 -*-
import logging
import requests
import os


from grab import Grab, DataNotFound
from grab.util.log import default_logging
from portal.list_portals import list_portals
from spamerBlog.celery import app
from django.contrib import messages
from portal.models import Portal


default_logging()
LOGGER = logging.getLogger('grab')
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


# Init grab
GRAB = Grab()


# //////////////// Auth portal ///////////////// #
def get_login_page(portal, login, password):
    """ Authenticate selected portal """
    url_login = portal['url_auth']
    GRAB.setup(timeout=10, connect_timeout=10, reuse_cookies=False)
    page_auth = GRAB.go(
        url_login, log_file='templates/grab/bug_auth_portal.html')
    page_auth.text_search(portal['auth_by'])
    return auth_portal(page_auth, portal, login, password)


def auth_portal(page_auth, portal, login, password):
    """ Authenticate selected portal """
    try:
        page_auth.set_input(portal['inp_login'], login)
        page_auth.set_input(portal['inp_password'], password)
        sub_resp = page_auth.submit()
        auth_form = sub_resp.text_search(portal['auth_complete'])
        if auth_form is True:
            return True
        else:
            return "Введите корректный логин или пароль"
    except DataNotFound:
        return "Вы уже аутентифицированы"


def go_authenticate(request, portal, login, password):
    login_page = get_login_page(portal, login, password)
    if login_page is True:
        messages.success(request, "Аутентификация прошла успешно!")
        return True
    else:
        messages.error(request, login_page)
        return False


# //////////////// Send spam ///////////////// #
def send_spam(input_data, portals):
    portals_list = get_selected_portal(portals)
    for p in range(len(portals_list)):
        GRAB.setup(timeout=10, connect_timeout=10)
        GRAB.go(
            portals_list[p]['url_auth'], log_file='templates/grab/bug_auth_portal.html', cookiefile='templates/grab/cookie.txt')
        GRAB.doc.set_input(portals_list[p]['inp_login'], 'denisoed')
        GRAB.doc.set_input(portals_list[p]['inp_password'], 'gorod312')
        GRAB.doc.submit()
        url_submit = portals_list[p]['url_submit']
        GRAB.setup(timeout=10, connect_timeout=10)
        GRAB.go(
            'https://www.reddit.com/submit', log_file='templates/grab/bug_submit.html', cookiefile='templates/grab/cookie.txt')
        # portal = fill_fields(GRAB, portals_list[p], input_data)
        GRAB.doc.set_input(
            portals_list[p]['inp_title'], 'Titit')
        GRAB.doc.set_input(
            portals_list[p]['inp_url'], 'https://gitlab.com/gen1us2k/poster/merge_requests/30/diffs')
        GRAB.doc.set_input(
            portals_list[p]['inp_text'], 'Description')
        GRAB.doc.submit()
    return True


def send(portal):
    response = portal.doc.submit()
    return response


def fill_fields(page, portal_input, input_data):
    page.doc.set_input(
        portal_input['inp_title'], input_data['title'])
    page.doc.set_input(
        portal_input['inp_url'], input_data['url'])
    page.doc.set_input(
        portal_input['inp_text'], input_data['description'])
    return page


def get_selected_portal(port_list):
    portals = []
    for i in range(len(port_list)):
        for p in range(len(list_portals)):
            if str(port_list[i]) == list_portals[p]['name']:
                portals.append(list_portals[p])
    return portals
