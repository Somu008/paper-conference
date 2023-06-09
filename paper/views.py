from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from authentication.utils import is_reviewer, get_reviewer_with_min_papers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings

from .models import Domain, Paper


def paper(request: HttpRequest):
    if request.method == "POST":
        Author_name = request.POST['Author_name']
        Co_author = request.POST['Co_author']
        Mname = request.POST['Mname']
        Institute = request.POST['Institute']
        domain = request.POST['domain']
        paper = request.FILES['paper']
        authors = [request.POST[f"co_author{i}"] for i in range(int(Co_author))]

        reviewer = get_reviewer_with_min_papers(domain)

        new_paper = Paper.objects.create(
            author_id=request.user,
            name=Author_name,
            authors = "\n".join(authors),
            mentor = Mname,
            institute = Institute,
            paper = paper,
            reviewer_id= reviewer,
            domain = Domain.objects.get(short_name=domain)
        )
        new_paper.save()

        reviewer.email_user("Kindly review the paper assigned to you..!", f"Paper with id {new_paper.pk} is assigned to you", settings.EMAIL_HOST_USER)

        return redirect(reverse('paper:paper_detail', args=[new_paper.pk]))
    return render(request, "authentication/upload_paper.html", { 'domains': Domain.objects.all() })

@login_required
def paper_detail(request, id):
    paper = get_object_or_404(Paper, pk=id)
    return render(request, 'paper/detail.html', {'paper': paper, 'is_reviewer': paper.reviewer_id == request.user})

@login_required
def papers(request):
    papers = []
    if is_reviewer(request.user):
        if request.user.reviewerprofile.state == 'pending':
            messages.error(request, 'Please complete your profile first')
            return redirect('reviewer:profile')

        papers = get_list_or_404(Paper, reviewer_id=request.user)
    else:
        papers = Paper.objects.filter(author_id=request.user.id)
    return render(request, "paper/all.html", { 'papers': papers })

@user_passes_test(is_reviewer)
def update_paper(request, id, action):
    paper = get_object_or_404(Paper, pk=id)

    paper.status = "approved" if action == "approve" else "rejected"


    paper.save()
    comment = request.POST.get("comment")
    paper.author_id.email_user("Status upadate on your paper..!", f"Paper with id {paper.pk} has been {paper.status}\n REASON: {comment}", settings.EMAIL_HOST_USER)

    return redirect("paper:paper_detail", id)

def stream_file(request, pk):
    paper = get_object_or_404(Paper, id=pk)
    response = HttpResponse()

    response['Content-Type'] = "application/pdf"
    response['Content-Length'] = len(paper.paper)
    response.write(paper.paper.read())
    return response
