from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):


    def create_user(self, phone_number, password = None, **extra_fields):

        email = extra_fields.get('email')
        if not phone_number:
            raise ValueError("Phone number is required")
        
        if not email:
            raise ValueError("Email is required")
        
        extra_fields['email'] = self.normalize_email(email)
        user = self.model(phone_number = phone_number, **extra_fields)

        user.set_password(password)
        user.save(using = self._db)

        return user
    

    def create_superuser(self, phone_number, password = None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone_number, password, **extra_fields)