from grab import Grab
import logging
from grab.util.log import default_logging
from portal.list_portals import list_portals
from django.contrib import messages

default_logging()
logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Init grab
grab = Grab()


def auth_portal(portal, log_pass, request):
    urlLogin = portal['url_auth']
    grab.setup(timeout=20, connect_timeout=20)
    grab.go(urlLogin, log_file='login.html')
    grab.doc.set_input(portal['inp_login'], log_pass['login'])
    grab.doc.set_input(portal['inp_password'], log_pass['password'])
    grab.doc.submit()
    if grab.response.code == 200: 
        messages.success(request, "Аутентификация прошла успешно!")
        return True
    else:
        messages.error(request, "Произошла ошибка!")
        return False
        
    
def send_spam(input_data, portals):
    for i in range(len(portals)):
        for p in range(len(list_portals)):
            if str(portals[i]) == list_portals[p]['name']:
                print(list_portals[p]['name'])
                urlSubmit = list_portals[p]['url_submit']
                grab.go(urlSubmit, log_file='submit.html')
                grab.doc.set_input(list_portals[p]['inp_title'], input_data['title'])
                grab.doc.set_input(list_portals[p]['inp_url'], input_data['url'])
                grab.doc.set_input(list_portals[p]['inp_text'], input_data['description'])
                grab.doc.submit()    

def handler_errors(error):    
    print(error)
