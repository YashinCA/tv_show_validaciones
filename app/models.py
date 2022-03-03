from platform import release
from django.db import models
from datetime import date, datetime, timedelta
from django.db.models.query import QuerySet


class TvshowManager(models.Manager):

    def basic_validator(self, postData):
        tvshows = Tvshow.objects.all()
        for show in tvshows:
            print(f'{show.id} {show.title}')
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        today = date.today().strftime('%Y-%m-%d')
        prueba = self.filter(
            title__iexact=postData['title'])
        # PARA EDITAR
        for value in prueba:
            if Tvshow.objects.get(id=value.id):
                print(Tvshow.objects.get(id=value.id).title)
                print('Si existe')
                if postData['releasedate'] > today:
                    errors['releasedate'] = "La fecha debe estar en el pasado"
                if len(postData['title']) < 2:
                    errors["title"] = "Title should be at least 2 characters"
                if postData['network'] == '':
                    errors["network1"] = "Please select or add a new network"
                if postData['network'] != 'otro':
                    if len(Network.objects.get(id=postData['network']).name) < 3:
                        errors["network"] = "Network should be at least 3 characters"
                else:
                    if len(postData['network-new']) < 3:
                        errors["network"] = "Network should be at least 3 characters"
                if (len(postData['description']) > 0) and (len(postData['description']) < 10):
                    errors["description"] = "Description is optional but to enter, it must have a minimum of 10 characters"
                print(Tvshow.objects.get(id=value.id).title)
                return errors
        # PARA CREAR
        if postData['releasedate'] > today:
            errors['releasedate'] = "La fecha debe estar en el pasado"
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        if self.filter(title__iexact=postData['title']).exists():
            errors['title'] = "Title already exists"
        if postData['network'] == '':
            errors["network1"] = "Please select or add a new network"
        if postData['network'] != 'otro':
            if len(Network.objects.get(id=postData['network']).name) < 3:
                errors["network"] = "Network should be at least 3 characters"
        else:
            if len(postData['network-new']) < 3:
                errors["network"] = "Network should be at least 3 characters"
        if (len(postData['description']) > 0) and (len(postData['description']) < 10):
            errors["description"] = "Description is optional but to enter, it must have a minimum of 10 characters"
        return errors


class Network(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # tvshows=lista de shows asociados al network


class Tvshow(models.Model):
    title = models.CharField(max_length=100, unique=True)
    network = models.ForeignKey(Network,
                                related_name="tvshows", on_delete=models.CASCADE)
    releasedate = models.DateField()
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TvshowManager()
