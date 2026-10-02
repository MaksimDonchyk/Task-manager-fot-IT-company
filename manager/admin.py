from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import Task, Position, TaskType, Worker, Team, Project


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    list_filter = ("group",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team")
    list_filter = ("team",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type", "project", "priority", "deadline", "is_completed")
    list_filter = ("is_completed", "priority", "task_type", "project")
    search_fields = ("name",)
