from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from models import Paper
from forms import PaperForm


def index(request):
    c = {}
    return render(request, "peer/index.html", c)


def paper_index(request):
    new_papers = Paper.objects.filter(published__isnull=False).order_by('-pk')[:10]
    c = {
        "papers": new_papers,
    }
    return render(request, "peer/paper_index.html", c)


def paper_detail(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    if request.user == paper.author or paper.is_public():
        c = {"paper": paper}
        return render(request, "peer/paper_detail.html", c)
    else:
        raise Http404("Paper does not exist.")


@login_required
def paper_submit(request):
    if request.method == "POST":
        paper = Paper(author=request.user)
        form = PaperForm(request.POST, request.FILES, instance=paper)

        if form.is_valid():
            form.save()
            # log
            return redirect(submission_index)
    else:
        form = PaperForm()

    c = {
        "form": form,
    }
    return render(request, "peer/submit_paper.html", c)


@login_required
def submission_index(request):
    c = {
        "papers": request.user.paper_set.all(),
    }
    return render(request, "peer/paper_index.html", c)

