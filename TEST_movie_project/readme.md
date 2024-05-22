
```bash
python manage.py shell_plus --print-sql

# create / update / delete
from movie_app.models import Movie

Movie(name='Test', rating=11).save()

t = Movie.objects.all()[1]

t.year = 2014
t.save()
t.delete()

# filter

```