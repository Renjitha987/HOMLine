from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_list_view, name='services_list'),
    path('services/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('membership/', views.membership_view, name='membership'),
    path('updates/', views.updates_list_view, name='updates_list'),
    path('updates/<slug:slug>/', views.update_detail_view, name='update_detail'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('contact/', views.contact_view, name='contact'),
    path('track/', views.track_request_view, name='track_request'),
    path('track/<str:request_id>/', views.track_request_view, name='track_request_with_id'),
    path('request/', views.request_service_view, name='request_service'),
    path('receipt/<str:request_id>/', views.receipt_view, name='receipt'),
    path('policy/<str:policy_name>/', views.policy_view, name='policy'),
]
