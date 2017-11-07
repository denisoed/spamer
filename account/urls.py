from django.conf.urls import url
from .views import registerUser, authorizationUser, logoutUser

urlpatterns = [
    url(r'register/$', registerUser, name='register user'),
    url(r'login/$', authorizationUser, name='authorization user'),
    url(r'logout/$', logoutUser, name='logout user'),
]
