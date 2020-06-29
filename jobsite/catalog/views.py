from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.db.models import Q

from .forms import RegisterForm, Apply, SearchForm
from .models import Industry, Company, JobVacancy, Application, City

# Create your views here.


def index(request):
    num_users = User.objects.all().count()
    num_companies = Company.objects.all().count()
    num_industries = Industry.objects.all().count()
    num_cities = City.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_users': num_users, 'num_companies': num_companies,
                 'num_industries': num_industries, 'num_cities': num_cities},
    )


class CompanyListView(generic.ListView):
    model = Company
    paginate_by = 10


class CompanyDetailView(generic.DetailView):
    model = Company


class IndustryListView(generic.ListView):
    model = Industry


class JobVacancyDetailView(generic.DetailView):
    model = JobVacancy


class JobVacancyListView(generic.ListView):
    model = JobVacancy
    paginate_by = 10


class IndustryDetailView(generic.DetailView):
    model = Industry


class AppliedVacancy(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/vacancy_applied_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)


def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }!')
            return redirect('/accounts/login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def renew(request, pk):
    vacancy = get_object_or_404(JobVacancy, pk = pk)
    application = Application()

    if request.method == 'POST':
        form = Apply(request.POST)

        if form.is_valid():
            application.applicant = request.user
            application.job = vacancy
            application.applied_on = form.cleaned_data['applied_on']
            application.save()
            return HttpResponseRedirect(reverse('my-application') )

    else:
        proposed_date = datetime.date.today()
        form = Apply(initial={'applied_on': proposed_date})

    return render(request, 'catalog/job_apply.html', {'form': form, 'application': application})


class SearchView(FormView):
    model = JobVacancy
    template_name = 'catalog/search.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('title')
        querydict = self.request.GET
        jobs = JobVacancy.objects.search_with_filters(querydict)
        if query:
            jobs = jobs.filter(
                Q(title__icontains=query)
            )
        context['jobs'] = jobs
        return context
