from django import forms
from django.contrib.auth.forms import get_user_model


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField()
 
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


