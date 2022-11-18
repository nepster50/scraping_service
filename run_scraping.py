import codecs

import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"


import django
django.setup()


from scr.scraping_service.parsers import *
from scraping.models import Vacancy, City, Language, Error

User = get_user_model()


parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=Київ&search=python'),
           (djinni, 'https://djinni.co/jobs/?region=UKR&location=kyiv&primary_keyword=Python'),
           (rabota, 'https://rabota.ua/ua/zapros/Python')
           )

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

#h = codecs.open('work.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()
