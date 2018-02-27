from django import forms

from user.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'age' , 'sex']

    password2 = forms.CharField(max_length=64)

    def is_valid(self):
        res = super().is_valid()
        return res and self.cleaned_data['password'] == self.cleaned_data['password2']
