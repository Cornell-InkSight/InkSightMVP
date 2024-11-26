from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from schoolmanagement.models import School

class UserManager(BaseUserManager):
    """Serializer For User Manager, based off of Auth Models"""
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser):
    """Generic User Model for Authentication"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser



class Student(User):
    """Student User Model with Additional Fields"""
    year = models.IntegerField()
    disability = models.CharField(max_length=666)
    sds_coordinator = models.ForeignKey(
        'SDSCoordinator', on_delete=models.SET_NULL, null=True, blank=True, related_name="students"
    )


class Professor(User):
    """Professor User Model with Additional Fields"""
    title = models.CharField(max_length=255) 


class TeacherAssistant(User):
    """Teacher Assistant User Model with Additional Fields"""
    assigned_professor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name="teacher_assistants"
    )


class SDSCoordinator(User):
    """SDS Coordinator User Model with Additional Fields"""
    position = models.CharField(max_length=255)
    access_code = models.CharField(max_length=8, unique=True)
