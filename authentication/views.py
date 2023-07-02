from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from authentication.models import ReviewerProfile
from capstone import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .utils import is_reviewer

def home(request: HttpRequest):
    ctx = {}
    if request.user.is_authenticated:
        ctx['user'] = request.user
    return render(request, "authentication/index.html", ctx)

def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('authentication:profile')

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user_type = request.POST['group']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('authentication:home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('authentication:home')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('authentication:home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('authentication:home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False


        if user_type == "group2":
            myuser.groups.add(Group.objects.get(name="Reviewers"))
            ReviewerProfile.objects.create(user=myuser).save()

        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Editorial Manager- Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Editorial Manager!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email- Editorial Login!!"
        message2 = render_to_string('email_confirmation.html',{

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('authentication:signin')


    return render(request, "authentication/signup.html")

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('authentication:signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('authentication:profile')

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        print("User", user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('authentication:profile')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('authentication:profile')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully!!")
    return redirect('authentication:home')

def paper_detail(request):
    return render(request, "authentication/paper_detail.html")

def profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "You're not signed in")
        return redirect('authentication:signin')

    if is_reviewer(request.user):
        return redirect("reviewer:profile")

    return redirect('authentication:home')
