from django import forms
from .models import MemberRSVP


class EventAttendeeForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = MemberRSVP
        fields = ('id', 'worked_on',)
