# -*- coding: utf-8 -*-
import logging
import requests


from grab import Grab, DataNotFound
from grab.util.log import default_logging
from portal.list_portals import list_portals
from spamerBlog.celery import app
from bs4 import BeautifulSoup


default_logging()
LOGGER = logging.getLogger('grab')
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)

# Init grab
GRAB = Grab()


def go_authenticate(request, portal, login, password):
    login_page = get_login_page(portal, login, password)
    if login_page is True:
        # messages.success(request, "Аутентификация прошла успешно!")
        return True
    else:
        # messages.error(request, login_page)
        return False


def get_login_page(portal, login, password):
    """ Authenticate selected portal """
    try:
        url_login = portal['url_auth']
        GRAB.setup(timeout=10, connect_timeout=10)
        response = GRAB.go(
            url_login, log_file='templates/grab/bug_auth_portal.html')
        response.text_search(portal['auth_by'])
        return auth_portal(response, portal, login, password)
    except DataNotFound:
        return "Ошибка при получении формы аутентификации. Попробуйте позже!"


def auth_portal(response, portal, login, password):
    """ Authenticate selected portal """
    try:
        response.set_input(portal['inp_login'], login)
        response.set_input(portal['inp_password'], password)
        sub_resp = response.submit()
        auth_form = sub_resp.text_search(portal['auth_complete'])
        if auth_form is True:
            return True
        else:
            return "Введите корректный логин или пароль"
    except DataNotFound:
        return "Вы уже аутентифицированы"


@app.task
def send_spam(input_data, portals):
    portals_list = get_selected_portal(portals)
    for p in range(len(portals_list)):
        url_submit = portals_list[p]['url_submit']
        parse_page = GRAB.go(
            url_submit, log_file='templates/grab/bug_submit.html')
        portal = fill_fields(parse_page, portals_list[p], input_data)
        send(portal)
    return True


def send(portal):
    portal.submit()
    return True


def fill_fields(page, portal_input, input_data):
    page.set_input(
        portal_input['inp_title'], input_data['title'])
    page.set_input(
        portal_input['inp_url'], input_data['url'])
    page.set_input(
        portal_input['inp_text'], input_data['description'])
    return page


def get_selected_portal(port_list):
    portals = []
    for i in range(len(port_list)):
        for p in range(len(list_portals)):
            if str(port_list[i]) == list_portals[p]['name']:
                portals.append(list_portals[p])
    return portals


# //////////////// Logout portal ///////////////// #
def logout_portal(portal):
    log_portal = get_selected_logout_portal(portal)
    resp_html = requests.post(log_portal['url_logout'])
    response = BeautifulSoup(resp_html.content, 'html.parser')
    block_for_html_btn = response.findAll("span", {"class": "pagetop"})
    print(block_for_html_btn)


def get_selected_logout_portal(portal):
    name_portal = portal[0]['name']
    for i in range(len(list_portals)):
        if list_portals[i]['name'] == name_portal:
            return list_portals[i]
        else:
            return False
