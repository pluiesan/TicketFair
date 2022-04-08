from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Event, Artist, Distributor, Tag
from django.db.models import Q
from datetime import datetime


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


class TagListView(ListView):
    model = Tag
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Event.objects.filter(is_published=True, tag=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'#{self.tag.name}'
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


class SearchEventListView(ListView):
    model = Event
    template_name = 'pages/list.html'
    # paginate_by = 2

    def get_queryset(self):
        self.query = self.request.GET.get('query') or ''
        queryset = super().get_queryset()

        if self.query:
            queryset = queryset.filter(
                Q(name__icontains=self.query) | Q(artist__name__icontains=self.query) | Q(distributor__name__icontains=self.query) 
            )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        self.event_count = len(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['event_count'] = self.event_count
        context["title"] = f"{self.query}の検索結果 {self.event_count}件"

        return context
