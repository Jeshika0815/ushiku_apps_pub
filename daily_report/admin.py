from django.contrib import admin
from .models import Employee, WorkLog


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_number', 'name', 'user')  # 表示するフィールド
    search_fields = ('employee_number', 'name', 'user__username')  # 検索フィールド

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'work_number', 'subject', 'date')  # 表示するフィールド
    search_fields = ('work_number', 'subject', 'employee__name')  # 検索フィールド
    list_filter = ('date', 'employee')  # フィルタリング可能なフィールド
