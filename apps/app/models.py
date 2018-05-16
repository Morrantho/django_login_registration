from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self,request):
		if len(request.POST["name"]) < 1:
			messages.add_message( request, messages.ERROR, "Name is required!" )
		if len(request.POST["email"]) < 1:
			messages.add_message( request, messages.ERROR, "Email is required!" )
		if not EMAIL_REGEX.match( request.POST["email"] ):
			messages.add_message( request, messages.ERROR, "Invalid email format! Ex: test@test.com" )
		if len(request.POST["password"]) < 8:
			messages.add_message( request, messages.ERROR, "Password must be between 8-32 characters!" )
		if request.POST["password"] != request.POST["confirm"]:
			messages.add_message( request, messages.ERROR, "Password and Password Confirmation must match!" )
		if User.objects.filter(email=request.POST["email"]).count() > 0:
			messages.add_message( request, messages.ERROR, "A user with this email already exists!" )

		if len( get_messages(request) ) > 0:
			return False
		else:
			User.objects.create(
				name = request.POST["name"],
				email = request.POST["email"],
				password = bcrypt.hashpw( request.POST["password"].encode() , bcrypt.gensalt() )
			)
			return True
			
	def login(self,request):
		pass

class User(models.Model):
	name     = models.CharField(max_length=255)
	email    = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects  = UserManager()