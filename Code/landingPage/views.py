from django.shortcuts import render
from adminPanel.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string


def landingPage(request):
    return render(request, 'landingPage.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"] #RERIEVING THE DETAILS ENTERED BY THE USER FROM LOGIN.HTML PAGE
        password = request.POST["password"] #RERIEVING THE DETAILS ENTERED BY THE USER FROM LOGIN.HTML PAGE
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if username == 'admin':
                login(request, user) #LOGIN FUNCTION USED TO LOGIN THE USER 
                # admin:index is predefined by djnago as the admin page name
                return redirect(reverse('admin:index'))  #REVERSE WILL CREATE AN URL FOE THE PARAMTER SPECIFIED 
            else:
                login(request, user) #LOGIN FUNCTION USED TO LOGIN THE USER 
                return redirect(reverse('home:home')) #REVERSE WILL CREATE AN URL FOE THE PARAMTER SPECIFIED 
        else:
            messages.error(request, "Incorrect Login Credentials!")
    return render(request, 'login.html')


def register_user(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        usernameExist = User.objects.filter(username=username)
        if usernameExist.exists():
            messages.warning(request, 'The username already exists!')
        else:
            user = User.objects.create_user(
                first_name=fname, last_name=lname, email=email, username=username, password=password)
            user.save()
            messages.success(request, "user registered successfully")
            return redirect('landingPage:login_user')
    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect('landingPage:login_user')


def verifyUser(request):
    if request.method == 'POST':
        userDetails = request.POST['userDetails']
        changePasswordurl = request.build_absolute_uri(
            reverse('landingPage:change_password')) + f'?userDetails={userDetails}'
        send_mail(
            "User Verification", #SUBJECT
            f"Please click on the link {changePasswordurl}' to change the password", #MESSAGE/BODY
            "tripcanvas30@gmail.com",#FROM 
            [userDetails]#TO
        )
    return render(request, 'verifyUser.html')


def change_password(request):
    email = request.GET['userDetails']
    if request.method == 'POST':
        newpassword1 = request.POST['password1']
        newpassword2 = request.POST['password2']
        userData = User.objects.get(email=email)
        if newpassword1 == newpassword2:
            userData.set_password(newpassword1)
            userData.save()
            messages.success(request, 'Password Changed Successfully')
        else:
            messages.error(request, 'Sorry! The passwords did not match')
        return redirect('landingPage:login_user')
    return render(request, 'changePassword.html')
