from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from paper.models import Domain

def is_reviewer(user):
    return user.groups.filter(name="Reviewers").exists()

def get_reviewer_with_min_papers(domain_name) -> User:
    domain = get_object_or_404(Domain, short_name=domain_name)
    domain_reviewers = domain.domains.all() # type: ignore

    free_reviewer, min_count = None, 100

    for reviewer in domain_reviewers:
        pending_paper_count = reviewer.user.reviewer.filter(status="pending").count()

        if pending_paper_count < min_count:
            free_reviewer, min_count = reviewer.user, pending_paper_count

    if free_reviewer is None:
        raise LookupError("BSDK khud review kr")

    return free_reviewer
