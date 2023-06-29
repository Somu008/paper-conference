from ast import Tuple
from pyexpat import model
from re import I
from django.core.mail import send_mail, mail_admins
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import models
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404
from authentication.models import ReviewerProfile

from authentication.utils import is_reviewer

User = auth.get_user_model()


@user_passes_test(is_reviewer)
@login_required
def profile(request: HttpRequest):
    rprofile = ReviewerProfile.objects.get_or_create(user = request.user)

    if request.method == "POST":
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']

        profession = request.POST.get('profession')
        institute = request.POST.get('ins_name')
        qualification = request.POST.get('H_Q')
        domain = request.POST.get('domain')

        resume = request.FILES.get('resume')


        user: models.AbstractUser = request.user # type: ignore

        user.first_name = f_name
        user.last_name = l_name
        user.email = email

        updates = {
                'state': "draft",
                'profession': profession,
                'institute': institute,
                'qualification': qualification,
                'domain': domain,
        }

        if resume:
            updates['resume'] = resume


        for key, val in updates.items():
            rprofile[0].__setattr__(key, val)

        rprofile[0].save()
        user.save()
        return redirect('reviewer:profile')

    return render(request, "Reviwer_detail/Reviewer_detail.html", { 'me': request.user, 'rprofile': rprofile[0] })

def submit_form(request):
    if request.method == 'POST':
        # Process the form data
        # Send email
        rprofile = ReviewerProfile.objects.get(user=request.user)
        rprofile.state = 'pending'
        rprofile.save()

        mail_admins(
            "Profile for review",
            f"Name: {request.user.first_name}\nEmail: {request.user.email}\nMessage: Hello, your details are pending for review."
        )

        messages.success(request, 'Details submitted successfully')

    # Render the form template for GET requests
    return redirect(reverse('authentication:profile'))


def stream_file(request):
    profile = get_object_or_404(ReviewerProfile, user=request.user)
    response = HttpResponse()

    response['Content-Type'] = "application/pdf"
    response['Content-Length'] = len(profile.resume)
    response.write(profile.resume.read())
    return response
