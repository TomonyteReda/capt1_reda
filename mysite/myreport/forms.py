from django import forms
from .models import DataFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('hash_checksum', 'file_contents', 'user', )
        widgets = {'hash_checksum': forms.HiddenInput(), 'user': forms.HiddenInput()}


class DateInput(forms.DateInput):
    input_type = 'date'


class UploadedFilesByUserListForm(forms.Form):
    from_ = forms.DateField(label="Upload Date From", required=False, widget=DateInput())
    to = forms.DateField(label="Upload Date To", required=False, widget=DateInput())

