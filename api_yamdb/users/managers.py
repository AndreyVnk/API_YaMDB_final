from django.contrib.auth.models import BaseUserManager

from .enums import Role


class CustomUserManager(BaseUserManager):
    """Class Custom manager."""

    def create_user(self, email, username, password=None, **args):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(
            username=username, email=self.normalize_email(email), **args)
        password = BaseUserManager.make_random_password(self)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **args):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, username, password, **args)
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.admin.value
        user.save()
        return user
