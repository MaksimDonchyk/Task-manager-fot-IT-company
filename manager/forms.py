from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from manager.models import Task, Worker, Position, TaskType, Team, Project


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "assignees",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and not (user.is_staff or user.is_superuser):
            user_teams = user.teams.all()

            if user_teams.exists():
                self.fields["task_type"].queryset = TaskType.objects.filter(
                    teams__in=user_teams
                ).distinct()

                self.fields["assignees"].queryset = Worker.objects.filter(
                    teams__in=user_teams
                ).distinct()


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 4:
            raise ValidationError("Name for position too short")
        return name


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Input type of task"}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "task_types", "members"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "task_types": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
            "members": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError("Назва команди занадто коротка.")
        return name


class ProjectForm(forms.ModelForm):

  class Meta:
    model = Project
    fields = ["name", "description", "team"]
    widgets = {
        "name": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть назву проєкту",
            }
        ),
        "description": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Короткий опис проєкту...",
            }
        ),
        "team": forms.Select(attrs={"class": "form-select"}),
    }

  def clean_name(self):
    name = self.cleaned_data.get("name")
    if name and len(name) < 3:
      raise ValidationError(
          "Назва проєкту повинна містити щонайменше 3 символи."
      )
    return name


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "position")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-select"}),
        }

    def save(self, commit=True):
        worker = super().save(commit=False)
        if commit:
            worker.save()
            if worker.position and worker.position.group:
                worker.groups.add(worker.position.group)
        return worker
