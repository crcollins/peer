from django import forms

from models import Paper

class PaperForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = ("title", "abstract", "pdf_file")

