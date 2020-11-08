from django.db import models


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