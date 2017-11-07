from django.conf.urls import url
from .views import main

urlpatterns = [
    url(r'main/$', main, name='main page'),
    url(r'send_spam/$', main, name='main page'),
]
