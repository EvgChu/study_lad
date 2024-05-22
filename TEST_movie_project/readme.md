
```bash

python manage.py shell_plus --print-sql

```

```python
# create / update / delete
from movie_app.models import Movie

Movie(name='Test', rating=11).save()

Movie.obgects.create(name='Test2', rating=11)

t = Movie.objects.all()[1]

t.year = 2014
t.save()
t.delete()

# filter
Movie.obgects.all()

Movie.obgects.get(id=3) # onle one

Movie.obgects.filter(year=3) # return QuerySet

Movie.obgects.filter(year__gt=3) # greater than
Movie.obgects.filter(year__lt=3) # less than
Movie.obgects.filter(year__gte=3) # greater than or equal 
Movie.obgects.filter(year__lte=3) # less than or equal 
Movie.obgects.filter(year__isnull=True)

Movie.obgects.filter(year__isnull=True, name='test') # AND
Movie.obgects.filter(name__contains='test') # LIKE '%test%'
Movie.obgects.filter(name__startswith='test') # LIKE 'test%'
Movie.obgects.filter(name__endswith='test') # LIKE '%test'

Movie.obgects.filter(id_in=(3, 4, 5)) # in (3, 4, 5)


Movie.obgects.exclude(year__lte=3)



```