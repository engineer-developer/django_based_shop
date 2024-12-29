from django import forms


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full name")
    age = forms.IntegerField(label="Your age", min_value=1, max_value=120)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)
