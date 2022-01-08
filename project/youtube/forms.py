from re import compile,match
from django import forms
from django.core.exceptions import ValidationError


REGEX = compile('^https://www.youtu')

class Getlink(forms.Form):

    CHOICHES = (
        ('video','Video'),
        ('audio','Audio'),
    )

    link = forms.CharField()
    choose = forms.ChoiceField(choices=CHOICHES)


    def clean_link(self):
        data = self.cleaned_data['link']
        custom_validate = match(REGEX,data)
        if not custom_validate:
            raise ValidationError("Please enter youtube link")
        return data