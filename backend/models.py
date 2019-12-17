from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
import datetime
import hashlib
import os
from django.utils.timezone import now
# Create your models here.
class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, name, password=None):
        mydate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')[:-3]
        actvString=mydate+'-activ'

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            activation=hashlib.md5(actvString.encode('utf-8')).hexdigest(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password):
        mydate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')[:-3]
        actvString=mydate+'-activ'
        user = self.create_user(
            email,
            password=password,
            name=name,
            activation=hashlib.md5(actvString.encode('utf-8')).hexdigest(),
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name= "True",
            activation=hashlib.md5(actvString.encode('utf-8')).hexdigest(),
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    activation = models.CharField(null=True,max_length=350)
    activated = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'name' ]
    def __str__(self):
        return self.email
    objects = UserManager()
