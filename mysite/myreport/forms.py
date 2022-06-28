from django import forms
from .models import DataFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('hash_checksum', 'file_contents', 'user', )
        widgets = {'hash_checksum': forms.HiddenInput(), 'user': forms.HiddenInput()}
