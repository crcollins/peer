from django import forms

from models import Paper, Revision

class PaperForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = ("title", "abstract")


class RevisionForm(forms.ModelForm):
    
    class Meta:
        model = Revision
        fields = ("comments", "pdf_file")
