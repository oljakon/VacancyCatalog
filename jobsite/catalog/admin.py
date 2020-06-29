from django.contrib import admin

# Register your models here.

from .models import City, Industry, Company, JobVacancy, Application, Resume

admin.site.register(City)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(JobVacancy)
admin.site.register(Application)
admin.site.register(Resume)
