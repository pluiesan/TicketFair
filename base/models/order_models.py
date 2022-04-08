from django.db import models
import datetime
from django.contrib.auth import get_user_model
from .ticket_models import Ticket
from django.utils.crypto import get_random_string

def create_id():
    return get_random_string(22)
 
def custom_timestamp_id():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')
 
 
class Order(models.Model):
    id = models.CharField(default=custom_timestamp_id,
                          editable=False, primary_key=True, max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uid = models.CharField(editable=False, max_length=50)
    is_confirmed = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=0)
    tax_included = models.PositiveIntegerField(default=0)
    canceled_at = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_pk = models.CharField(default='', max_length=50)
    event_name = models.CharField(default='', max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
 
    def __str__(self):
        return self.id


class MyTicket(models.Model):
    id = models.CharField(default=create_id,
                          editable=False, primary_key=True, max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uid = models.CharField(editable=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(default='', max_length=50)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, null=False, blank=False)
    reference_number = models.IntegerField(default=0)
 
    def __str__(self):
        return self.id