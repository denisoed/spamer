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
        url_submit = portals_list[p]['url_submit']
        GRAB.go(
            url_submit, log_file='templates/grab/bug_submit.html')
        portal = fill_fields(GRAB, portals_list[p], input_data)
        send(portal)
    return True


def send(portal):
    response = portal.doc.submit()
    return response


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
