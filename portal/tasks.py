# -*- coding: utf-8 -*-
import logging
from django.contrib import messages
from grab import Grab, DataNotFound
from grab.util.log import default_logging
from portal.list_portals import list_portals


default_logging()
LOGGER = logging.getLogger('grab')
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)

# Init grab
GRAB = Grab()


def get_login_page(request, portal, login, password):
    """ Authenticate selected portal """
    try:
        url_login = portal['url_auth']
        print(url_login)
        GRAB.setup(timeout=10, connect_timeout=10)
        GRAB.go(url_login, log_file='templates/grab/bug_auth_portal.html')
        GRAB.doc.text_search(portal['auth_by'])
        auth_portal(request, portal, login, password)
        return True
    except DataNotFound:
        messages.error(
            request, "Ошибка при получении формы аутентификации. "
                     "Попробуйте позже!")
        return False


def auth_portal(request, portal, login, password):
    """ Authenticate selected portal """
    try:
        GRAB.doc.set_input(portal['inp_login'], login)
        GRAB.doc.set_input(portal['inp_password'], password)
        GRAB.doc.submit()
        auth_form = GRAB.doc.text_search(portal['auth_complete'])
        if auth_form is True:
            messages.success(request, "Аутентификация прошла успешно!")
            return True
        else:
            messages.error(request, "Введите корректный логин или пароль!")
            return False
    except DataNotFound:
        messages.error(request, "Вы уже аутентифицированы!")
        return False


def send_spam(input_data, portals):
    portals_list = get_selected_portal(portals)
    for p in range(len(portals_list)):
        url_submit = portals_list[p]['url_submit']
        GRAB.go(url_submit, log_file='templates/grab/bug_submit.html')
        GRAB.doc.set_input(
            portals_list[p]['inp_title'], input_data['title'])
        GRAB.doc.set_input(
            portals_list[p]['inp_url'], input_data['url'])
        GRAB.doc.set_input(
            portals_list[p]['inp_text'], input_data['description'])
        GRAB.doc.submit()
    return GRAB.response.code


def get_selected_portal(port_list):
    portals = []
    for i in range(len(port_list)):
        for p in range(len(list_portals)):
            if str(port_list[i]) == list_portals[p]['name']:
                portals.append(list_portals[p])
    return portals
