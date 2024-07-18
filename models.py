from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class EmployeeManager(BaseUserManager):
    def create_user(self, empid, name, email, password=None):
        if not empid:
            raise ValueError('The EmpId field must be set')
        employee = self.model(empid=empid, name=name, email=self.normalize_email(email))
        employee.set_password(password)
        employee.save(using=self._db)
        return employee


class Employee(AbstractBaseUser):
    empid = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'empid'
    REQUIRED_FIELDS = ['name', 'email']

    objects = EmployeeManager()

    def __str__(self):
        return self.empid
