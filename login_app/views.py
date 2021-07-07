from django.shortcuts import render, redirect
from imgfield_app.models import User, Quote
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST": 
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("/signon")
        
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
        
        if not User.objects.all():
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password=pw_hash,
                security_level = 5
            ) 
        else:
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password=pw_hash,
                security_level = 1
            ) 
        request.session['user_id'] = user.id
        return redirect("/")   
    else:
        return redirect("/signon")


def login(request):
    if request.method == "POST": 
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("/signon")
        else:
            user = User.objects.get(email = request.POST['lemail'])
            if bcrypt.checkpw(request.POST['lpassword'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect("/")
            else:
                return redirect("/signon")
    else:
        return redirect("/signon")


def logout(request):
    if 'open_quote' in request.session:
        quote = Quote.objects.get(id=request.session['open_quote'])
        quote.delete()
    request.session.flush()
    return redirect("/")
