from django.contrib import admin
from .models import User, Student, SystemAdmin, BuildingEstateDepartment, AccommodationOfficeDepartment, Complaint, Feedback, Message, ComplainReport, ActivityLog

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_accomodation', 'is_student', 'is_building_estate', 'is_system_admin']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'course', 'reg_no', 'phone_no', 'room_name', 'created_at']


@admin.register(SystemAdmin)
class SystemAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone', 'created_at']


@admin.register(BuildingEstateDepartment)
class BuildingEstateDepartmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'department_head', 'department_name', 'created_at']


@admin.register(AccommodationOfficeDepartment)
class AccommodationOfficeDepartmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'department_head', 'department_name', 'created_at']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['subject', 'description', 'student', 'created_at', 'status', 'location']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'message', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'receiver', 'sender']


@admin.register(ComplainReport)
class ComplainReportAdmin(admin.ModelAdmin):
    list_display = ['Title_complaint', 'staff_name', 'location', 'budget', 'toolname', 'created_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('actor', 'action_type', 'action_time', 'status', 'remarks')
    list_filter = ('action_type', 'status', 'action_time')
    search_fields = ('actor__username', 'remarks')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('actor')
