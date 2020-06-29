from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import City, Industry, Company, Resume

error_username = {
    'required': 'Пожалуйста, заполните это поле!',
    'max_length': 'Имя не может превышать 20 символов!',
    'min_length': 'Имя должно быть больше 2 символов!'
}

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

'''class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50,min_length=3,error_messages=error_username)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    rep_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput)'''


class Apply(forms.Form):
    applied_on = forms.DateField(help_text="This is the date of your application. We'll save it")
    def clean_renewal_date(self):
        data = self.cleaned_data['applied_on']
        return data


class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False,)
    industry = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Industry.objects.all(),required=False,label="Industry")
    city = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=City.objects.all(),required=False,label="City")
    company = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Company.objects.all(),required=False,label="Company")


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['birth_date', 'education', 'description']