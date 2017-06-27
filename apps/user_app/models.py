from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
	def create_user(self, email, username, first_name, last_name, password):
		self.create(email=email, username=username, first_name=first_name, last_name=last_name, password=password)

	def hash_password(self, password):
		hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		return hashed_pw

	def compare_passwords(self, user, password):
		password = password.encode()
		hashed_pw = user.password.encode()
		if bcrypt.hashpw(password, hashed_pw) == hashed_pw:
			return True
		else:
			return False

	def validateregister(self, data):
		password = data['password']
		errors = []
		if len(data['email'])<=1:
			errors.append('Email cannot be blank.')
		if len(data['username'])<=1:
			errors.append('Username cannot be blank.')
		if len(data['first_name'])<1:
			errors.append('First name cannot be left empty.')
		if len(data['last_name'])<1:
			errors.append('Last name cannot be left empty.')
		if len(password)<=7:
			errors.append('Password must contain at least eight characters')
		if password != data['confirm_password']:
			errors.append('Passwords do not match.')
		if self.filter(email=data['email']).exists():
			errors.append('Whoops! Looks like that email is already in our database')
		if errors:
			return (False, errors)
		else:
			pw_hash = self.hash_password(password)
			user = self.create_user(data['email'], data['username'], data['first_name'], data['last_name'], pw_hash)
			print user
			return (True, user)

	def validatelogin(self, data):
		errors = []
		if len(data['email'])<1:
			errors.append('Please include an email in order to log in.')
		if len(data['password'])<1:
			errors.append('Please input your password in order to log in.')
		if errors:
			return (False, errors)
		try:
			user = self.get(email=data['email'])
			if self.compare_passwords(user, data['password']):
				print user
				return (True, user)
			else:
				errors.append("Password does not match account")
				return(False, errors)
		except:
			errors.append('Whoops! Looks like your account does not yet exist')
			return (False, errors)

class User(models.Model):
	email = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	first_name = models.CharField(max_length=55)
	last_name = models.CharField(max_length=55)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	