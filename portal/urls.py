from django.conf.urls import url
from portal.views import create_portal, delete_portal

urlpatterns = [
    url(r'create/$', create_portal, name='create_portal'),
    url(r'delete/(?P<id_portal>\d+)/$', delete_portal, name='delete_portal'),
]
