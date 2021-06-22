from django import forms

def clean_name(self):
    name = self.cleaned_data['name']
    if len(name) < 4:
        raise forms.ValidationError("name is too short")
    return name  