from django.conf.urls import url
from portal.views import createPortal

urlpatterns = [
    url(r'create/$', createPortal, name='create portal'),
]
