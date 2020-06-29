from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('industry-detail', args=[str(self.id)])


class Company(models.Model):
    name = models.CharField(max_length = 50)
    industry = models.ManyToManyField(Industry)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])


class JobVacancyManager(models.Manager):
    def search_with_filters(self, querydict):
        jobs = self.all()
        params = ['industry', 'city', 'company']
        for param in params:
            for item in querydict.getlist(param):
                if param == 'industry':
                    jobs = jobs.filter(industry__id=item)
                elif param == 'city':
                    jobs = jobs.filter(city__id=item)
                elif param == 'company':
                    jobs = jobs.filter(company__id=item)
        return jobs


class JobVacancy(models.Model):
    title = models.CharField(max_length = 100)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey('Industry', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)

    YEARS_OF_EXP = (
        ('entry', 'Entry level'),
        ('1-2', '1-2 years'),
        ('3-5', '3-5 years'),
        ('6-10', '6-10 years'),
        ('above 10', 'Above 10 years')
    )

    years_of_exp = models.CharField('Years of Experience', max_length=20, choices=YEARS_OF_EXP, null=True, blank=True)

    TYPES = (
        ('fulltime', 'Full-Time'),
        ('parttime', 'Part-Time')
    )

    type = models.CharField(max_length=10, choices=TYPES)

    objects = JobVacancyManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(JobVacancy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('job-vacancy-detail', args=[str(self.id)])


class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey('JobVacancy', on_delete=models.SET_NULL, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.applicant.last_name

    def get_absolute_url(self):
        return reverse('application-detail', args=[str(self.id)])


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name = 'coverletter')
    birth_date = models.DateTimeField()
    education = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.user.last_name

    def get_absolute_url(self):
        return reverse('resume-detail', args=[str(self.id)])