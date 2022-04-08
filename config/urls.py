"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('guest_login/', views.guest_login, name='guest_login'),
    
 
    # Order
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),
    path('orders/', views.OrderIndexView.as_view()),
    path('my_ticket/', views.MyTicketView.as_view()),
    path('ticket_detail/<str:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
 
    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view()),
    path('pay/success/', views.PaySuccessView.as_view()),
    path('pay/cancel/', views.PayCancelView.as_view()),
 
    # Events
    path('events/<str:pk>/', views.EventDetailView.as_view()),
    path('artists/<str:pk>/', views.ArtistListView.as_view()),
    path('distributors/<str:pk>/', views.DistributorListView.as_view()),
    path('tag/<str:pk>/', views.TagListView.as_view()),


    path('', views.IndexListView.as_view(), name="index"),
    path ('search/', views.SearchEventListView.as_view(), name='search-event-list')
]
