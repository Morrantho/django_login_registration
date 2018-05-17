from __future__ import unicode_literals
from django.shortcuts import render,redirect

from .models import User,Author,Book,Review

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
	latestReviews = Review.objects.all().order_by("-id")[:3]
	otherReviews = Review.objects.all().order_by("-id")[3:];

	context = {
		"reviews":latestReviews,
		"otherReviews":otherReviews
	}

	return render(request,"app/books.html",context);

def addBook(request):
	authors = Author.objects.all()
	return render(request,"app/addBook.html",{
		"authors":authors
	})

def createBook(request):
	if len(request.POST["author"]) < 1 and len( request.POST["newAuthor"] ) < 1:
		messages.add_message(request,messages.ERROR,"You need to supply an author name!"); 
		return redirect("/books");

	if request.POST["author"]:
		author = int(request.POST["author"])

	newAuthor = "";

	if len( request.POST["newAuthor"] ) > 0:
		newAuthor = Author.objects.create(
			name = request.POST["newAuthor"]
		)
		author = newAuthor.id	

	book = Book.objects.create(
		title = request.POST["title"],
		author_id = author
	)

	review = Review.objects.create(
		text = request.POST["review"],
		rating = request.POST["rating"],
		user_id = 1,
		book_id = book.id
	);

	return redirect("/books");

def showBook(request,id):
	book = Book.objects.get(id=id);
	reviews = Review.objects.filter(book_id=id);

	context = {
		"book":book,
		"reviews":reviews
	}
	return render(request,"app/showBook.html",context);