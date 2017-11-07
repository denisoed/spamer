from grab import Grab
import logging
from grab.util.log import default_logging
default_logging()
from portal.list_portals import list_portals

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Init grab
grab = Grab()


def register_user(portal, log_pass):
    urlLogin = portal['url_auth']
    grab.setup(timeout=20, connect_timeout =20)
    grab.go(urlLogin, log_file='login.html')
    grab.doc.set_input(portal['inp_login'], log_pass['login'])
    grab.doc.set_input(portal['inp_password'], log_pass['password'])
    grab.doc.submit()
    if grab.response.code == 200:
        print('Authentication!')
    else:
        print('Error')    
    
def send_spam(input_data, portals):
    for i in range(len(portals)):
        for p in range(len(list_portals)):
            if str(portals[i]) == list_portals[p]['name']:
                print(list_portals[p]['name'])
                urlSubmit = list_portals[p]['url_submit']
                grab.go(urlSubmit, log_file='submit.html')
                grab.doc.set_input(list_portals[p]['inp_title'], input_data['title'])
                grab.doc.set_input(list_portals[p]['inp_url'], input_data['url'])
                # grab.doc.set_input(input_data[i].input_description, input_data[i].description)
                grab.doc.submit()    

def handler_errors(error):    
    print(error)
