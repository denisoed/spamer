import factory
from django.contrib.auth.models import User

class UserAuthFactory(factory.Factory):
    class Meta:
        model = User

    username = 'testuser',
    password1 = 'qwerty123'
    password2 = 'qwerty123'
    
