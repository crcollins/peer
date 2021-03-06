import random
import hashlib
import math

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from peer.models import Review, Paper, PENDING


def hash_file(f, blocksize=65536):
    buf = f.read(blocksize)
    hasher = hashlib.sha256()
    while len(buf) > 0:
        hasher.update(buf)
        buf = f.read(blocksize)
    return hasher.hexdigest()


def reviewer_classifier(paper):
    if paper.title == "accepted": return 3
    return random.randint(1, 3)


def editor_classifier(paper, reviews):
    average = sum(x.decision for x in reviews) / float(len(reviews))
    editor_revs = sum(1 for x in reviews if x.editor)
    rev_bonus = 2. / (1 + math.exp(-2 * editor_revs)) - 1
    editor = (random.random() - 0.5) / 4.0 + rev_bonus
    print editor, average
    return int(round(average + editor))


def reviewer_response(paper):
    return "This is a message from a reviewer."


def editor_response(paper, reviews):
    return "This is a message from the editor."


class Command(BaseCommand):
    help = 'Add reviews for all the current pending papers'

    def handle(self, *args, **kwargs):
        reviewer = User.objects.get(username="reviewer")
        editor = User.objects.get(username="editor")
        for paper in Paper.objects.filter(status=PENDING):
            print paper
            rev = paper.revisions.latest()
            if not rev.hash_value:
                rev.hash_value = hash_file(rev.pdf_file)
                rev.save()

            random.seed(int(rev.hash_value, 16))
            for x in xrange(random.randint(2,5)):
                print "rev", x,
                decision = reviewer_classifier(paper)
                comments = reviewer_response(paper)
                print decision
                Review(
                    paper=paper,
                    author=reviewer,
                    comments=comments,
                    decision=decision,
                ).save()

            print "ed", paper,
            reviews = paper.reviews.all()
            decision = editor_classifier(paper, reviews)
            comments = editor_response(paper, reviews)
            print decision
            Review(
                paper=paper,
                author=editor,
                editor=True,
                comments=comments,
                decision=decision,
            ).save()
            paper.update_status(decision)
