from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from manager.forms import (
    TaskForm,
    PositionForm,
    TaskTypeForm,
    WorkerCreationForm,
    TeamForm,
    ProjectForm
)
from manager.models import (
    Task,
    Worker,
    Position,
    TaskType,
    Team,
    Project
)


class TeamLeadRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=["Team Leads", "Project Managers (PM)"]).exists()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser or user.groups.filter(name__in=["Team Leads", "Project Managers (PM)"]).exists():
            return queryset

        return queryset.filter(assignees=user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, TeamLeadRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser or request.user.is_team_lead()):
            return redirect("manager:task-list")
        return super().dispatch(request, *args, **kwargs)


class TaskUpdateView(LoginRequiredMixin, TeamLeadRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")


class TaskChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get("status")

        if new_status == "review":
            pass
        elif new_status in ["approved", "rejected"]:
            if not request.user.is_team_lead():
                return redirect("manager:task-detail", pk=task.pk)
        else:
            # Якщо передано невідомий статус — повертаємося назад
            return redirect("manager:task-detail", pk=task.pk)

        if new_status in dict(Task.StatusChoices.choices):
            task.status = new_status

            if new_status == "approved":
                task.is_completed = True
            else:
                task.is_completed = False

            task.save()

        return redirect("manager:task-detail", pk=task.pk)


class WorkerListView(TeamLeadRequiredMixin, ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "manager/worker_detail.html"
    context_object_name = "worker"


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("manager:worker-list")


class PositionListView(ListView):
    model = Position
    template_name = "manager/position_list.html"
    context_object_name = "position_list"
    paginate_by = 5


class PositionCreateView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = "manager/position_form.html"
    success_url = reverse_lazy("manager:position-list")


class TaskTypeListView(ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5


class TaskTypeCreateView(CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")


class TeamListView(ListView):
    model = Team
    template_name = "manager/team_list.html"
    context_object_name = "team_list"
    paginate_by = 5


class TeamDetailView(DetailView):
    model = Team
    template_name = "manager/team_detail.html"
    context_object_name = "team"


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "manager/team_form.html"
    success_url = reverse_lazy("manager:team-list")

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect("manager:team-list")
        return super().dispatch(request, *args, **kwargs)


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'manager/team_form.html'
    success_url = reverse_lazy('manager:team-list')


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'manager/team_confirm_delete.html'
    success_url = reverse_lazy('manager:team-list')


class ProjectListView(ListView):
    model = Project
    template_name = "manager/project_list.html"
    context_object_name = "project_list"
    paginate_by = 5


class ProjectDetailView(DetailView):
    model = Project
    template_name = "manager/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
  model = Project
  fields = ["name", "description", "team"]
  template_name = "manager/project_form.html"
  success_url = reverse_lazy("manager:project-list")

  def dispatch(self, request, *args, **kwargs):
    if not (request.user.is_staff or request.user.is_superuser):
      return HttpResponseForbidden("Тільки Project Manager може створювати проєкти.")
    return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    fields = ["name", "description", "team"]
    template_name = "manager/project_form.html"
    success_url = reverse_lazy("manager:project-list")


class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = "manager/project_confirm_delete.html"
    success_url = reverse_lazy("manager:project-list")
