from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse

from task_manager_project import settings


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="positions",
        help_text="Група дозволів, яка буде автоматично надана працівникам цієї посади."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})

    def is_team_lead(self):
        if self.is_staff or self.is_superuser:
            return True
        if self.position and "lead" in self.position.name.lower():
            return True
        return False

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    task_types = models.ManyToManyField(
        TaskType,
        related_name="teams",
        blank=True,
        help_text="Типи завдань, на яких спеціалізується ця команда."
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Team: {self.team.name})"


class Task(models.Model):
  class PriorityChoises(models.TextChoices):
    BLOCKER = "Blocker", "Blocker"
    CRITICAL = "Critical", "Critical"
    MAJOR = "Major", "Major"
    MINOR = "Minor", "Minor"
    TRIVIAL = "Trivial", "Trivial"

  class StatusChoices(models.TextChoices):
    IN_PROGRESS = "in_progress", "В роботі"
    REVIEW = "review", "На рев'ю"
    APPROVED = "approved", "Заапрувлено"
    REJECTED = "rejected", "Відхилено"

  name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  deadline = models.DateField()
  is_completed = models.BooleanField(default=False)
  priority = models.CharField(
      max_length=20,
      choices=PriorityChoises.choices,
      default=PriorityChoises.MAJOR,
  )
  status = models.CharField(
      max_length=20,
      choices=StatusChoices.choices,
      default=StatusChoices.IN_PROGRESS,
  )
  task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT, related_name="tasks")
  project = models.ForeignKey(
      Project,
      on_delete=models.CASCADE,
      related_name="tasks",
      null=True,
      blank=True,
  )
  assignees = models.ManyToManyField(
      settings.AUTH_USER_MODEL,
      related_name="tasks",
      blank=True
  )

  class Meta:
      ordering = ["deadline"]

  def __str__(self):
    status_icon = "✅" if self.is_completed else "⏳"
    return f"{status_icon} {self.name} (Deadline: {self.deadline})"

  def get_absolute_url(self):
    return reverse("manager:task-detail", kwargs={"pk": self.pk})