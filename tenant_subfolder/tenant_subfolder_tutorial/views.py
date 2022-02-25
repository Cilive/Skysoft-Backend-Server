import django
from django.conf import settings
from django.db import utils
from django.views.generic import TemplateView
from django_tenants.utils import remove_www
from customers.models import Client
from rest_framework_simplejwt.views import TokenObtainPairView

# from tenant_subfolder_tutorial.administrator.models import User

from .serielizer import ComapanyTokenObtainPairSerializer

# from django.contrib.auth import get_user_model
# from django.db.models import Q


# class AuthBackend(object):
#     supports_object_permissions = True
#     supports_anonymous_user = False
#     supports_inactive_user = False


#     def get_user(self, user_id):
#        try:
#           return User.objects.get(pk=user_id)
#        except User.DoesNotExist:
#           return None


#     def authenticate(self, username, password):
#         try:
#             user = User.objects.get(
#                 Q(username=username) | Q(email=username) | Q(phone=username)
#             )
#         except User.DoesNotExist:
#             return None

#         return user if user.check_password(password) else None
class CompanyTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComapanyTokenObtainPairSerializer

