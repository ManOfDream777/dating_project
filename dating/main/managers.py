from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

class MyUserManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создание пользователя по имени, фамилии, email и паролю
        """
        name = extra_fields.get('first_name')
        surname = extra_fields.get('last_name')
        gender = extra_fields.get('gender')
        if not name and not surname and not gender:
            raise ValueError("The given credentials must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
