from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from models import Paper, Revision, PENDING
from forms import PaperForm, RevisionForm


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
        paper_form = PaperForm(request.POST, instance=paper)
        rev = Revision(paper=paper)
        rev_form = RevisionForm(request.POST, request.FILES, instance=rev)
        
        # prevent short circuit
        paper_valid = paper_form.is_valid()
        rev_valid = rev_form.is_valid()
        

        if paper_valid and rev_valid:
            new_paper = paper_form.save()
            rev = Revision(paper=new_paper)
            rev_form = RevisionForm(request.POST, request.FILES, instance=rev)
            rev_form.save()
            # log
            return redirect(submission_index)
    else:
        paper_form = PaperForm()
        rev_form = RevisionForm()

    c = {
        "paper_form": paper_form,
        "rev_form": rev_form,
    }
    return render(request, "peer/submit_paper.html", c)


@login_required
def submission_index(request):
    c = {
        "papers": request.user.paper_set.all(),
    }
    return render(request, "peer/paper_index.html", c)


def revision_submit(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id, author=request.user)
    if request.method == "POST":
        revision = Revision(paper=paper)
        form = RevisionForm(request.POST, request.FILES, instance=revision)

        if form.is_valid():
            form.save()
            paper.update_status(PENDING)
            # log
            return redirect(submission_index)
    else:
        form = RevisionForm()

    c = {
        "form": form,
    }
    return render(request, "peer/submit_revision.html", c)
