from django.urls import path
from . import apis

urlpatterns = [
    path('attendance/get_qr/', apis.get_qr, name='kiosk'),
    path('attendance/status/<str:token>/', apis.status, name='kiosk_status'),
    path('attendance/confirm/<str:token>/', apis.confirm, name='mobile_confirm'),
    path('attendance/records/', apis.records_list, name='records'),
]
