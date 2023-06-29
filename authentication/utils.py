from django.contrib.auth.models import User

def is_reviewer(user):
    return user.groups.filter(name="Reviewers").exists()

def get_reviewer_with_min_papers() -> User:
    # filter with domain
    reviewers = User.objects.filter(is_superuser=False, groups__name="Reviewers")

    reviewer, min_count = None, 100

    for user in reviewers:
        pending_paper_count = user.reviewer.filter(status="pending").count()

        if pending_paper_count < min_count:
            reviewer, min_count = user, pending_paper_count

    if reviewer is None:
        raise LookupError("BSDK khud review kr")

    return reviewer
