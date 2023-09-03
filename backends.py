from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(surname=username)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
