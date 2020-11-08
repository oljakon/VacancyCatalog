from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import City, Industry, Company, Resume


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ApplyForm(forms.Form):
    applied_on = forms.DateField(help_text="This is the date of your application. We'll save it")

    def clean_renewal_date(self):
        data = self.cleaned_data['applied_on']
        return data


class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False, )
    industry = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Industry.objects.all(),
                                              required=False, label="Industry")
    city = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=City.objects.all(),
                                          required=False, label="City")
    company = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Company.objects.all(),
                                             required=False, label="Company")


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['birth_date', 'education', 'description']
