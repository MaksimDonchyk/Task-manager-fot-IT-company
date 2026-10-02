from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from manager.forms import (
    TaskForm,
    PositionForm,
    TaskTypeForm,
    WorkerCreationForm,
    TeamForm,
    ProjectForm
)
from manager.models import Task, Worker, Position, TaskType, Team, Project


class TaskListView(ListView):
    model = Task
    template_name = "manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5


class TaskDetailView(DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")


class WorkerListView(ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 5


class WorkerDetailView(DetailView):
    model = Worker
    template_name = "manager/worker_detail.html"
    context_object_name = "worker"


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "manager/worker_form.html"
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


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = "manager/team_form.html"
    success_url = reverse_lazy("manager:team-list")


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
    form_class = ProjectForm
    template_name = "manager/project_form.html"
    success_url = reverse_lazy("manager:project-list")
