import random
import hashlib

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from peer.models import Review, Paper, PENDING


def hash_file(f, blocksize=65536):
    buf = f.read(blocksize)
    hasher = hashlib.sha256()
    while len(buf) > 0:
        hasher.update(buf)
        buf = f.read(blocksize)
    return int(hasher.hexdigest(), 16)


def reviewer_classifier(paper):
    if paper.title == "accepted": return 3
    return random.randint(1, 3)


def editor_classifier(paper, reviews):
    average = sum(x.decision for x in reviews) / float(len(reviews))
    editor = (random.random() - 0.5) / 4.0
    return int(round(average + editor))


def reviewer_response(paper):
    return "This is a message from a reviewer."


def editor_response(paper, reviews):
    return "This is a message from the editor."


class Command(BaseCommand):
    help = 'Add reviews for all the current pending papers'

    def handle(self, *args, **kwargs):
        USER = User.objects.all()[0]
        for paper in Paper.objects.filter(status=PENDING):
            print paper
            random.seed(hash_file(paper.pdf_file))
            for x in xrange(random.randint(2,5)):
                print "rev", x,
                decision = reviewer_classifier(paper)
                comments = reviewer_response(paper)
                print decision
                Review(
                    paper=paper,
                    author=USER,
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
                author=USER,
                editor=True,
                comments=comments,
                decision=decision,
            ).save()
            paper.update_status(decision)
