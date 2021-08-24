from django.db import models
import re

from django.db.models.deletion import CASCADE
class UserManager(models.Manager):
    def register_validation(self, post_data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        #validate first name
        if len(post_data['first_name']) < 2 :
            errors['first_name_length'] = "First name has at least 2 characters."
        if not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "First name must be letters!"

        #validate last name
        if len(post_data['last_name'])< 2:
            errors['last_name_length'] = "Last name has at least 2 characters."
        if not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Last name must be letters!"

        #validate email
        users = User.objects.filter(email = post_data['email'])
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if users:
            errors['email_used'] = "This emaill address has registered by someone else."

        #validate password
        if len(post_data['password']) < 8:
            errors['password_length'] = "Password has at least 8 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['password_not_match'] = "Password Not Match!!!"
        return errors

    def login_validation(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # users = User.objects.exclude(email = post_data['email'])
        # if users:
        #     errors['email_not_register'] = "This email address not register yet!!! Go to register"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if post_data['password'] == '':
            errors['password_empty'] = "Password is required!"
        
        return errors

class BookManager(models.Manager):
    def book_validation(self,post_data):
        errors={}

        if post_data['title'] == '':
            errors['title'] = "Title is required!!"

        if len(post_data['desc']) < 5:
            errors['des'] = "Description has at least 5 characters."

        return errors



# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = "liked_books")
    objects = BookManager()