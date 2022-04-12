from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from base.models import Event, Artist, Distributor, Tag, Bookmark
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexListView(ListView):
    model = Event
    template_name = 'pages/index.html'

    def get_queryset(self):
        return Event.objects.filter(is_published=True)


class EventDetailView(DetailView):
    model = Event
    template_name = 'pages/event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            bookmark = Bookmark.objects.filter(event=context['event'], user=self.request.user)
            if bookmark.exists():
                context['bookmarked'] = True
            else:
                context['bookmarked'] = False
        return context


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
    model = Event
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


class BookmarkListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(user=self.request.user)
        bookmark_list = [bookmark.event.id for bookmark in bookmarks]
        return Event.objects.filter(is_published=True, id__in=bookmark_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ブックマークしたイベント'
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


class BookmarkView(View):
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=request.POST.get('event_id'))
        user = request.user
        bookmarked = False
        bookmark = Bookmark.objects.filter(event=event, user=user)
        if bookmark.exists():
            bookmark.delete()
        else:
            bookmark.create(event=event, user=user)
            bookmarked = True
    
        context = {
            'event_id': event.id,
            'bookmarked': bookmarked,
            # 'count': bookmark.like_set.count(),
        }

        return JsonResponse(context)
