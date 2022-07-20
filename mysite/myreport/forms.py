from django import forms
from .models import DataFile
from django.utils.translation import gettext_lazy as _


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('hash_checksum', 'file_contents', 'user', )
        widgets = {'hash_checksum': forms.HiddenInput(), 'user': forms.HiddenInput()}


class DateInput(forms.DateInput):
    input_type = 'date'


class UploadedFilesByUserListForm(forms.Form):
    from_ = forms.DateField(label=_("Upload Date From"), required=False, widget=DateInput())
    to = forms.DateField(label=_("Upload Date To"), required=False, widget=DateInput())


class ModelReportFilterForm(forms.Form):
    from_ = forms.DateField(label=_("Log Date From"), required=False, widget=DateInput())
    to = forms.DateField(label=_("Log Date To"), required=False, widget=DateInput())
    uploaded = forms.DateField(label=_("Upload Date"), required=False, widget=DateInput())

