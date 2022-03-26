from django.db import models
from django.utils.crypto import get_random_string
import os


def create_id():
    return get_random_string(22)


def upload_image_to(instance, filename):
    item_id = instance.id
    return os.path.join('static', 'items', item_id, filename)


class Artist(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Distributor(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    name = models.CharField(default='', max_length=50)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

class Event(models.Model):
    id = models.CharField(default=create_id, primary_key=True,
                          max_length=22, editable=False)
    name = models.CharField(default='', max_length=50)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(default='', blank=True)
    event_time = models.DateTimeField(auto_now_add=True)
    place = models.CharField(default='', blank=True, max_length=50)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default="static/images/logo.png", blank=True,
                              upload_to=upload_image_to)
    artist = models.ManyToManyField(Artist)
    distributor = models.ForeignKey(
        Distributor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

