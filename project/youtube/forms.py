from django import forms


class Getlink(forms.Form):

    CHOICHES = (
        ('video','Video'),
        ('audio','Audio'),
    )

    link = forms.CharField()
    choose = forms.ChoiceField(choices=CHOICHES)