from django import forms

from toldi.models import LogMessage
from toldi.models import CNjoke

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)  # NOTE: the trailing comma is required


class CNjokeForm(forms.ModelForm):
    class Meta:
        model = CNjoke
        fields = ("jokeEN","jokeHU",)  # NOTE: the trailing comma is required
