from .models import CustomerUser, ComeAndWent, Feedback
from django.contrib.auth.models import Group, User
from django.contrib import admin


admin.site.unregister([Group, User])


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'username', 'group_name', 'phone_number', 'registration_date', 'is_active')
    list_filter = ('group_name', 'is_active')
    search_fields = ('user_id', 'first_name', 'last_name', 'username', 'group_name')
    ordering = ('-is_active',) 

class ComeAndWentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'time_to_come', 'time_to_go', 'late_reason', 'absent_reason', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__user_id', 'user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'feedback_text', 'submission_time')
    list_filter = ('user', 'submission_time')
    search_fields = ('user__user_id', 'user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'


admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(ComeAndWent, ComeAndWentAdmin)
admin.site.register(Feedback, FeedbackAdmin)

