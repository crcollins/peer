import random


def reviewer_classifier(paper):
    return random.randint(0, 2)


def editor_classifier(paper, reviews):
    average = sum(reviews) / float(len(reviews))
    editor = (random.random() - 0.5) / 4.0
    return round(average + editor)


def reviewer_response(paper):
    return "This is a message from a reviewer."


def editor_response(paper, reviews):
    return "This is a message from the editor."

