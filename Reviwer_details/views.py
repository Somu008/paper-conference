from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

def submit_form(request):
    if request.method == 'POST':
        # Process the form data
        # Send email
        user = request.user
        subject = 'Form Submitted'
        message = f"Name: {user.first_name}\nEmail: {user.email}\nMessage: Hello, your details are pending for review."
        from_email = settings.EMAIL_HOST_USER  # Sender's email address
        to_email = 'sbsharma@mitaoe.ac.in'  # Admin's email address

        send_mail(subject, message, from_email, [to_email])
        messages.success(request, 'Details submitted successfully')

    # Render the form template for GET requests
    return redirect(reverse('authentication:profile'))
