# -*- coding: utf-8 -*-
import logging


from grab import Grab
from grab.util.log import default_logging
from portal.list_portals import list_portals
from celery.task import task

default_logging()
LOGGER = logging.getLogger('grab')
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


# Init grab
GRAB = Grab()


# //////////////// Send spam ///////////////// #
@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def send_spam(input_data, portals):
    portals_list = get_selected_portal(portals)
    for p in range(len(portals_list)):
        GRAB.setup(timeout=10, connect_timeout=10)
        url_auth = portals_list[p]['url_auth']
        GRAB.go(url_auth, log_file='templates/grab/bug_auth_portal.html')
        GRAB.doc.set_input(portals_list[p]['inp_login'], input_data['login'])
        GRAB.doc.set_input(portals_list[p]['inp_password'],
                           input_data['password'])
        GRAB.doc.submit()
        GRAB.setup(timeout=10, connect_timeout=10)
        url_submit = portals_list[p]['url_submit']
        GRAB.go(
            url_submit,
            log_file='templates/grab/bug_submit.html')
        GRAB.doc.set_input(
            portals_list[p]['inp_title'], input_data['title'])
        GRAB.doc.set_input(
            portals_list[p]['inp_url'], input_data['url'])
        GRAB.doc.set_input(
            portals_list[p]['inp_text'], input_data['description'])
        # send(GRAB)
    return True


def send(portal):
    response = portal.doc.submit()
    return response


def get_selected_portal(port_list):
    portals = []
    for i in range(len(port_list)):
        for p in range(len(list_portals)):
            if str(port_list[i]) == list_portals[p]['name']:
                portals.append(list_portals[p])
    return portals
