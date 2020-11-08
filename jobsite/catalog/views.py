from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.db.models import Q

from .forms import RegisterForm, ApplyForm, SearchForm
from .models import Industry, Company, JobVacancy, Application, City


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        num_users = User.objects.all().count()
        num_companies = Company.objects.all().count()
        num_industries = Industry.objects.all().count()
        num_cities = City.objects.all().count()
        context = {'num_users': num_users, 'num_companies': num_companies,
                   'num_industries': num_industries, 'num_cities': num_cities}
        return context


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


class RegisterView(generic.FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}!')
        return super().form_valid(form)


class Apply(generic.View):
    form_class = ApplyForm
    initial = {'applied_on': datetime.date.today()}
    template_name = 'catalog/job_apply.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        vacancy = get_object_or_404(JobVacancy, pk=self.kwargs['pk'])
        application = Application()
        return render(request, self.template_name, {'form': form, 'application': application, 'jobvacancy': vacancy})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        vacancy = get_object_or_404(JobVacancy, pk=self.kwargs['pk'])
        application = Application()
        if form.is_valid():
            application.applicant = request.user
            application.job = vacancy
            application.applied_on = form.cleaned_data['applied_on']
            application.save()
            return HttpResponseRedirect(reverse('my-application'))


class SearchView(generic.FormView):
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
