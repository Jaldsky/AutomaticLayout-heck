from enum import Enum

from django import forms
from app.models import AuthUser, UserUploadFile
from app.utils.common import get_uuid, extract_extension


class ErrorMessages(str, Enum):
    EMAIL_ALREADY_EXIST = 'Email already registered!'
    PASSWORDS_SYNC_CONFIRM = 'Passwords do not match, please enter passwords again!'

    def __str__(self) -> str:
        return str.__str__(self)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(ErrorMessages.PASSWORDS_SYNC_CONFIRM)

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError(ErrorMessages.EMAIL_ALREADY_EXIST)
        return email

    def save(self, commit=True):
        form = super(UserRegistrationForm, self).save(commit=False)
        form.set_password(self.cleaned_data["password"])

        if commit:
            form.save()
        return form


class UserUploadFileForm(forms.ModelForm):

    class Meta:
        model = UserUploadFile
        fields = ['file']

    def save(self, commit=True):
        form = super(UserUploadFileForm, self).save(commit=False)
        form.file_type = extract_extension(str(form.file))
        form.uuid = get_uuid()

        if commit:
            form.save()
        return form
