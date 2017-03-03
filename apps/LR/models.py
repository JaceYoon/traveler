from django.db import models
from datetime import date
import re,bcrypt
# Create your models here.

class UserManager(models.Manager):
    def ValidForm(self, userData):
        errors = []
        if not userData['name'].isalpha():
            errors.append('Your name should be characters')
        if len(userData['name']) < 3:
            errors.append('Name must be at least 3 characters')
        if len(userData['username']) < 3:
            errors.append('Username must be at least 3 characters!')
        check_username = self.filter(username = userData['username'])
        if check_username:
            errors.append('Sorry .. Your Username is already exists!')
        if not len(userData['password']):
            errors.append('Please enter the Password')
        if len(userData['password']) < 8:
            errors.append('Password must be at least 8 long')
        if not userData['password'] == userData['confirm']:
            errors.append('Passwords must match!')


        modelsResponse = {}

        if errors:
            modelsResponse['isRegistered'] = False
            modelsResponse['errors'] = errors
        else:
            hashed_password = bcrypt.hashpw(userData['password'].encode(), bcrypt.gensalt())
            user = self.create(name = userData['name'],username = userData['username'], password = hashed_password)
            modelsResponse['isRegistered'] = True
            modelsResponse['user'] = user

        return modelsResponse

    def login_user(self, userData):
        user = self.filter(username = userData['username'])
        errors = []
        modelsResponse = {}
        if not user:
            errors.append('Invalid username')
        else:
            if bcrypt.checkpw(userData['password'].encode(), user[0].password.encode()):
                modelsResponse['isLoggedIn'] = True
                modelsResponse['user'] = user[0]

            else:
                errors.append('Username or Password is not correct')

        if errors:
            modelsResponse['isLoggedIn'] = False
            modelsResponse['errors'] = errors

        return modelsResponse


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
