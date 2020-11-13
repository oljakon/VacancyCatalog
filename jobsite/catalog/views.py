from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RegisterForm, ApplyForm, SearchForm
from .models import Industry, Company, JobVacancy, Application, City
from .repository import RegisterLogic, AppliedVacancyLogic, ApplyLogic, SearchLogic


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
        query = AppliedVacancyLogic.get_applications_by_user(self, self.model)
        return query


class RegisterView(generic.FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        RegisterLogic.register_user(form)
        return super().form_valid(form)


class Apply(generic.View):
    form_class = ApplyForm
    initial = {'applied_on': datetime.date.today()}
    template_name = 'catalog/job_apply.html'
    application = Application()

    def get(self, request, *args, **kwargs):
        data = ApplyLogic.get_application(self)
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        ApplyLogic.post_application(self, request)
        return HttpResponseRedirect(reverse('my-application'))


class SearchView(generic.FormView):
    model = JobVacancy
    template_name = 'catalog/search.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_page = SearchLogic.get_data(self, context)
        return search_page
