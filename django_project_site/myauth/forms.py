from django import forms

from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "avatar",
        ]


class AboutMeAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]
