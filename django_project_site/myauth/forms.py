from django import forms

from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "avatar",
        ]

    email = forms.EmailField()


class AboutMeAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]
