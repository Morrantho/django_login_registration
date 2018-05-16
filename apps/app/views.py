from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
	return render(request,"app/index.html");

def register(request):
	if request.method == "POST":
		User.objects.register(request);
		return redirect("/");
	else:
		return redirect("/");

def login(request):
	try:
		user = User.objects.get( email=request.POST["email"] );

		isValid = bcrypt.checkpw( request.POST["password"].encode() , user.password.encode() )

		print(isValid)
 
		if isValid:
			print("PASSWORDS MATCH");
			return redirect("/books");
		else:
			print("NO MATCH");
			messages.add_message( request, messages.ERROR, "Invalid Credentials!" );
			return redirect("/");
	except:
		messages.add_message( request, messages.ERROR, "No user with this email was found!" );
		return redirect("/");

def books(request):
	return render(request,"app/books.html");




