from .models import MuroUser
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class MuroUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MuroUser.objects.filter(Q(email=username) | Q(phone_number=username), is_active=True).first()
        except MuroUser.DoesNotExist:
            return None
        if user and user.check_password(password):
            return user
        return None
    

    def get_user(self, user_id):
        try:
            return MuroUser.objects.get(pk=user_id)
        except MuroUser.DoesNotExist:
            return None