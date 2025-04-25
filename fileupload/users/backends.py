from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find the user by username or email (case insensitive)
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # If no user is found, return None
            return None
        except UserModel.MultipleObjectsReturned:
            # In case of multiple matching records (shouldn't happen if the data is clean)
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # Validate the password and check if the user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None  # Return None if authentication fails
