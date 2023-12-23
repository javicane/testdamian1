from django import forms

class UPloadGIDREPORTForm(forms.Form):
    file = forms.FileField(label='Select the file from your local computer')