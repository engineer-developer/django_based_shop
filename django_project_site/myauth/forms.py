from django import forms

from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "avatar",
        ]

    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["email"].initial = self.instance.user.email


class AboutMeAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]
