from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.station_list, name='station_list'),
    path('stations/<str:station_id>/', views.station_detail, name='station_detail'),
    path('stations/<str:station_id>/status/', views.update_station_status, name='update_status'),
]