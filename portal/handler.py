import logging
from grab import Grab, DataNotFound
from grab.util.log import default_logging
from .list_portals import list_portals
from django.contrib import messages

default_logging()
LOGGER = logging.getLogger('grab')
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)

# Init grab
GRAB = Grab()

def auth_portal(portal, log_pass, request):
    """ Authenticate selected portal """
    try:
        url_login = portal['url_auth']
        GRAB.setup(timeout=10, connect_timeout=10)
        GRAB.go(url_login, log_file='login.html')
        GRAB.doc.text_search(portal['auth_by'])
        try:
            GRAB.doc.set_input(portal['inp_login'], log_pass['login'])
            GRAB.doc.set_input(portal['inp_password'], log_pass['password'])
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
    except DataNotFound:
        messages.error(request, "Ошибка при получении формы аутентификации. Попробуйте позже!")
        return False

def send_spam(input_data, portals):
    """ Send spam to all selected portals """
    for i in range(len(portals)):
        for p in range(len(list_portals)):
            if str(portals[i]) == list_portals[p]['name']:
                print(list_portals[p]['name'])
                url_submit = list_portals[p]['url_submit']
                GRAB.go(url_submit, log_file='submit.html')
                GRAB.doc.set_input(list_portals[p]['inp_title'], input_data['title'])
                GRAB.doc.set_input(list_portals[p]['inp_url'], input_data['url'])
                GRAB.doc.set_input(list_portals[p]['inp_text'], input_data['description'])
                GRAB.doc.submit()
