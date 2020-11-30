from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^company/$', views.CompanyListView.as_view(), name='company'),
    url(r'^company/(?P<pk>\d+)$', views.CompanyDetailView.as_view(), name='company-detail'),
    url(r'^industry/$', views.IndustryListView.as_view(), name='industry'),
    url(r'^industry/(?P<pk>\d+)$', views.IndustryDetailView.as_view(), name='industry-detail'),
    url(r'^jobvacancy/(?P<pk>\d+)$', views.JobVacancyDetailView.as_view(), name='job-vacancy-detail'),
    url(r'^jobvacancy/(?P<pk>\d+)/job-apply', views.Apply.as_view(), name='job-apply'),
    url(r'^myapplication/$', views.AppliedVacancy.as_view(), name='my-application'),
    url(r'^search/', views.SearchView.as_view(), name='search'),
]
