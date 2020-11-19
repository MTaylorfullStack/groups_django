from django.db import models
import re


class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="First name must be longer than 2 characters!"
        if len(postdata['l_n'])<2:
            errors['l_n']="Last name must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be valid format!"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters!"
        if postdata['password'] != postdata['confirm_password']:
            errors['confirm_password']="Password and confirm password must match!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class OrgManager(models.Manager):
    def validator(self, postdata):
        errors={}
        if len(postdata['name'])<5:
            errors['name']="Org name is too short."
        if len(postdata['description'])<10:
            errors['desc']="Description must be longer."
        return errors

class Org(models.Model):
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    members=models.ManyToManyField(User, related_name="orgs")
    creator=models.ForeignKey(User, related_name="created_orgs", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=OrgManager()


