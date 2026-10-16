from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from manager.forms import (
    ProjectForm,
    TaskForm,
    TeamForm,
    WorkerCreationForm
)
from manager.models import Project, Task, Team, Worker


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser or user.has_perm("manager.view_all_tasks") or user.groups.filter(name__in=["Group_1", "Group_3"]).exists():
            return queryset

        return queryset.filter(assignees=user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    permission_required = "manager.add_task"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")
    permission_required = "manager.change_task"


class TaskChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get("status")

        if new_status == "review":
            pass
        elif new_status in ["approved", "rejected"]:
            if not (request.user.is_superuser or request.user.has_perm("manager.change_task")):
                return redirect("manager:task-detail", pk=task.pk)
        else:
            return redirect("manager:task-detail", pk=task.pk)

        if new_status in dict(Task.StatusChoices.choices):
            task.status = new_status
            task.is_completed = (new_status == "approved")
            task.save()

        return redirect("manager:task-detail", pk=task.pk)


class WorkerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 5
    permission_required = "manager.view_worker"


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "manager/worker_detail.html"
    context_object_name = "worker"


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("manager:worker-list")


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "manager/team_list.html"
    context_object_name = "team_list"
    paginate_by = 5


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "manager/team_detail.html"
    context_object_name = "team"


class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "manager/team_form.html"
    success_url = reverse_lazy("manager:team-list")
    permission_required = "manager.add_team"


class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'manager/team_form.html'
    success_url = reverse_lazy('manager:team-list')
    permission_required = "manager.change_team"


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Team
    template_name = 'manager/team_confirm_delete.html'
    success_url = reverse_lazy('manager:team-list')
    permission_required = "manager.delete_team"


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "manager/project_list.html"
    context_object_name = "project_list"
    paginate_by = 5


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "manager/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"
    success_url = reverse_lazy("manager:project-list")
    permission_required = "manager.add_project"


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"
    success_url = reverse_lazy("manager:project-list")
    permission_required = "manager.change_project"


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "manager/project_confirm_delete.html"
    success_url = reverse_lazy("manager:project-list")
    permission_required = "manager.delete_project"
