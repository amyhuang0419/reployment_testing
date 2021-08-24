from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
import bcrypt
from .models import User, Book

# Create your views here.
def index(request):
    return render(request, 'login_and_register.html')

def register(request):
    errors = User.objects.register_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value)
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/')
    
    return redirect('/')

def login(request):
    errors = User.objects.login_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value)
    else:
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
            else:
                messages.error(request, "Email or Password not match!!!")
        if not user:
            messages.error(request,"This email address not register yet!!! Go to register")

    return redirect('/')

def mainpage(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['user_id']),
            'books': Book.objects.all()
        }
        return render(request, 'main_page.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def create_book(request):
    errors = Book.objects.book_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value)    

    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user
        )
        user.liked_books.add(book)
        return redirect('/books')
    
    return redirect('/books')

def display_book(request, book_id):
    book = Book.objects.get(id=book_id)
    context= {
        'book' : book,
        'logged_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'book_details.html', context)

def update(request,book_id):
    errors = Book.objects.book_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value)    
        return redirect(f'/books/{book_id}')
    else:
        update_book = Book.objects.get(id = book_id)
        update_book.title = request.POST['title']
        update_book.desc = request.POST['desc']
        update_book.save()

        return redirect('/books')

def delete(request, book_id):
    delete_book = Book.objects.get(id=book_id)
    delete_book.delete()
    return redirect('/books')

def favorite(request,book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect(f'/books/{book_id}')

def all_fav(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'books': user.liked_books.all()
    }
    return render(request,'user_page.html',context)