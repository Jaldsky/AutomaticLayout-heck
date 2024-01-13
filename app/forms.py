from django import forms
from app.models import UploadedFile


class FileUploadForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()

    class Meta:
        model = UploadedFile
        fields = ('file',)
