from re import compile,match
from django import forms
from django.core.exceptions import ValidationError


REGEX = compile(r'^https://www.youtu')
REGEX2 = compile(r'^https://youtu')

class Getlink(forms.Form):

    CHOICHES = (
        ('video','Video'),
        ('audio','Audio'),
    )

    link = forms.CharField()
    choose = forms.ChoiceField(choices=CHOICHES)


    def clean_link(self):
        data = self.cleaned_data['link']
        custom_validate,custom_validate2 = match(REGEX,data) ,match(REGEX2,data)
        if not custom_validate or not custom_validate2:
            raise ValidationError("Please enter youtube link")
        return data