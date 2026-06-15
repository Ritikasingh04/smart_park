from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_index, name='index'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('api/slots/', views.slot_status_api, name='slot_api'),
]
