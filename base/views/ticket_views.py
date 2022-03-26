from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Event, Artist, Distributor


class IndexListView(ListView):
    model = Event
    template_name = 'pages/index.html'

    def get_queryset(self):
        return Event.objects.filter(is_published=True)
 

class EventDetailView(DetailView):
    model = Event
    template_name = 'pages/event.html'

class ArtistListView(ListView):
    model = Event
    template_name = 'pages/list.html'
    paginate_by = 2
 
    def get_queryset(self):
        self.artist = Artist.objects.get(slug=self.kwargs['pk'])
        return Event.objects.filter(is_published=True, artist=self.artist)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'出演者 #{self.artist.name}'
        return context
 
 
class DistributorListView(ListView):
    model = Event
    template_name = 'pages/list.html'
    paginate_by = 2
 
    def get_queryset(self):
        self.distributor = Distributor.objects.get(slug=self.kwargs['pk'])
        return Event.objects.filter(is_published=True, distributor=self.distributor)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"販売元 #{self.distributor.name}"
        return context