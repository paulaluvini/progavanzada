from django import forms

class EmailForm(forms.Form):
        email = forms.CharField(label='Email', max_length=100)
