from django.conf.urls import url
from portal.views import create_portal, delete_portal
from .tasks import get_login_page


urlpatterns = [
    url(r'create/$', create_portal, name='create_portal'),
    url(r'delete/(?P<id_portal>\d+)/$', delete_portal, name='delete_portal'),
    url(r'get_login_page/(?P<portal>\w+)$',
        get_login_page, name='get_login_page')
]
