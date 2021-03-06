from base.forms import UserCreationForm
from django.contrib import admin
from base.models import Event, Ticket, Artist, Distributor, User, Order, MyTicket, Tag, Bookmark
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_active', 'is_admin',)}),
    )
 
    list_display = ('username', 'email', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
 
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active',)}),
    )
 
    add_form = UserCreationForm
 

class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline, ]

  
admin.site.register(Order)
admin.site.register(Event, EventAdmin)
admin.site.register(MyTicket)
admin.site.register(Ticket)
admin.site.register(Artist)
admin.site.register(Distributor)
admin.site.register(Tag)
admin.site.register(Bookmark)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)