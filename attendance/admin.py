from django.contrib import admin
from .models import sessionModel
from .models import attendanceModel

@admin.register(sessionModel.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('token','created_at','verified','verified_by','expires_at')
    search_fields = ('token',)

@admin.register(attendanceModel.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user','timestamp','device', 'signin_at','signout_at')
    search_fields = ('user__username','device','signin_at','signout_at')
