from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from models import Paper
from forms import PaperForm

def index(request):
    c = {}
    return render(request, "peer/index.html", c)


def paper_index(request):
    # public papers only
    new_papers = Paper.objects.get_recent(10)
    c = {
        "papers": new_papers,
    }
    return render(request, "peer/paper_index.html", c)


def paper_detail(request, paper_id):
    paper = Paper.objects.get(id=paper_id)
    if paper and paper.is_public:
        return render(request, paper)
    else:
        return render(request, 404)
    
@login_required
def paper_submit(request):
    if request.method == "POST":
        paper = Paper(author=request.user)
        form = PaperForm(request.POST, request.FILES, instance=paper)

        if form.is_valid():
            form.save()
            # log
            return redirect(index)
    else:
        form = PaperForm()

    c = {
        "form": form,
    }
    return render(request, "peer/submit_paper.html", c)


@login_required
def review_submissions(request):
    c = {
        "papers": request.user.papers,
    }
    return render(request, "peer/review_submissions.html", c)


@login_required
def review_submission_detail(request, paper_id):
    c = {
        "paper": Paper.objects.get(paper_id),
    }
    return render(request, "peer/review_submission_detail.html", c)

