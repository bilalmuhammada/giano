from django.contrib import admin
from .models import Session, Attendance


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('token','created_at','verified','verified_by','expires_at')
    search_fields = ('token',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user','timestamp','device')
    search_fields = ('user__username','device')
