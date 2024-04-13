from django import forms

from django.contrib.auth.models import User

# from app.models import UploadedFile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            User.objects.create(user=user)
        return user


# class FileUploadForm(forms.ModelForm):
#     # title = forms.CharField(max_length=50)
#     # file = forms.FileField()
#
#     class Meta:
#         model = UploadedFile
#         fields = ('file',)
