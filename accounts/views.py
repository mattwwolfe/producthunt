from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    #check if the request is a POST, which is the result of clicking the login button
    if request.method == 'POST':
        #check if the passwords match
        if request.POST['password1'] == request.POST['password2']:
            #check if the username was already taken
            try:
                user = User.objects.get(username = request.POST['username'])
                #if the name is already taken send back to sign up page with error message
                return render(request, 'accounts/signup.html', {'error':'Sorry that username has already been taken.'})
            #if username is free then write the username and password to the database, log them in, and send to home page
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        #if the passwords didn't match, then send back to sign-up page with error
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match.'})
    #if request was a GET, then render the signup page
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    #check if the request is a POST, which is the result of clicking the login button
    if request.method == 'POST':
        #try and authenticate the user
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        #if authentication was successfull log them in and redirect to home page
        if user is not None:
            auth.login(request, user)
            return redirect ('home')
        #if authentication failed then send back to login page with an error message
        else:
            return render(request, 'accounts/login.html', {'error':'Username or Password is incorrect'})
    #if the request is a GET then render the login page
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    #check if request is a POST
    if request.method == 'POST':
        #log them out and send them to home page
        auth.logout(request)
        return redirect('home')
