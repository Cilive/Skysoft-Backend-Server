import email
from administrator.models import User
from django.db import connection


from django.contrib.auth import get_user_model
from django.db.models import Q


# User = get_user_model()

class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, request, username=None, password=None, **kwargs):
       print("get user working")
       try:
          return User.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
      
       except User.DoesNotExist:
           
          return None


    def authenticate(self, request, email=None, password=None, **kwargs):
      
        try:
            user = User.objects.get(
                Q(username=email) | Q(email=email) | Q(phone=email)
            )
            print(connection.queries)
            print("user found ",user)
            
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None