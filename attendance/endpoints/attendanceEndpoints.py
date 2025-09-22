from django.urls import path
from ..apis import attendanceApi as apis

urlpatterns = [
    path('attendance/get_qr/', apis.get_qr, name='get_qr'),
    path('attendance/status/<str:token>/', apis.status, name='status'),
    path('attendance/get_code/<str:token>/', apis.get_code, name='get_code'),
    path('attendance/confirm/<str:token>/', apis.confirm, name='confirm'),
    path('attendance/records/', apis.records_list, name='records'),
]
