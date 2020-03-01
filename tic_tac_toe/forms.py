from django import forms

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config


class NameForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=config.MAX_NAME_LENGTH,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'autocomplete': 'off',
            'size': config.MAX_NAME_LENGTH,
            'placeholder': 'Enter Name'
        }))
