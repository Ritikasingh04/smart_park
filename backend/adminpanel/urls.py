from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('slots/', views.slots_view, name='slots'),
    path('users/', views.users_view, name='users'),
    path('bookings/', views.bookings_view, name='bookings'),
    path('revenue/', views.revenue_view, name='revenue'),
]
