
from django.contrib.auth.models import  BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        print(extra_fields)
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:  
            user.set_password(password)
        
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,   **extra_fields):
        user = self.create_user(email, password=password,)
        user.is_superuser = True  
        user.is_staff = True 
        user.role='admin'
        user.save(using=self._db)
        return user