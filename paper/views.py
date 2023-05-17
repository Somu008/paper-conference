from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from .models import Paper
# from . tokens import generate_token

def paper(request):
    if request.method == "POST":
        Author_name = request.POST['Author_name']
        Co_author = request.POST['Co_author']
        Mname = request.POST['Mname']
        Institute = request.POST['Institute']
        domain = request.POST['domain']
        paper = request.POST['paper']

        myuser = Paper.objects.create(
            author_id=request.user,
            name=Author_name,
            authors = Co_author,
            mentor = Mname,
            institute = Institute,
            paper = paper
            
        )
        myuser.save()

        return redirect(reverse('paper:paper_detail', args=[myuser.pk]))
    return render(request, "authentication/upload_paper.html")

def paper_detail(request, id):
    paper = get_object_or_404(Paper, pk=id)

    return render(request, 'paper/detail.html', { paper: paper })
