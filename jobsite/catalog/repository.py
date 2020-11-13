from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import JobVacancy


class RegisterLogic():
    @staticmethod
    def register_user(form):
        form.save()
        username = form.cleaned_data.get('username')


class AppliedVacancyLogic():
    @staticmethod
    def get_applications_by_user(self, model):
        return model.objects.filter(applicant=self.request.user)


class ApplyLogic():
    @staticmethod
    def get_application(self):
        form = self.form_class(initial=self.initial)
        vacancy = get_object_or_404(JobVacancy, pk=self.kwargs['pk'])
        data = {'form': form, 'application': self.application, 'jobvacancy': vacancy}
        return data

    @staticmethod
    def post_application(self, request):
        form = self.form_class(request.POST)
        data = get_object_or_404(JobVacancy, pk=self.kwargs['pk'])
        if form.is_valid():
            self.application.applicant = request.user
            self.application.job = data
            self.application.applied_on = form.cleaned_data['applied_on']
            self.application.save()


class SearchLogic():
    @staticmethod
    def get_data(self, context):
        query = self.request.GET.get('title')
        querydict = self.request.GET
        jobs = JobVacancy.objects.search_with_filters(querydict)
        if query:
            jobs = jobs.filter(
                Q(title__icontains=query)
            )
        context['jobs'] = jobs
        return context