from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from manager.models import Team, Position, Project, Task, TaskType
from manager.forms import TeamForm, TaskForm  # За потреби імпорти твоїх форм

User = get_user_model()


class FullProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Python Developer")
        self.task_type = TaskType.objects.create(name="Bugfix")

        self.admin = User.objects.create_superuser(
            username="admin_boss",
            password="securepassword123"
        )

        self.worker = User.objects.create_user(
            username="test_worker",
            password="password123",
            position=self.position,
            first_name="Олег",
            last_name="Коваленко"
        )

        self.team = Team.objects.create(name="Code Cats")
        self.team.members.add(self.worker)

    def test_custom_user_model_fields_and_position(self):
        user = User.objects.get(username="test_worker")
        self.assertEqual(user.position.name, "Python Developer")
        self.assertEqual(user.first_name, "Олег")
        self.assertEqual(user.last_name, "Коваленко")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)

    def test_team_form_validation_invalid(self):
        form_data = {"name": "", "members": [self.worker.pk]}
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors, "Форма повинна вимагати назву команди")

    def test_team_form_validation_valid(self):
        form_data = {"name": "New Awesome Team", "members": [self.worker.pk]}
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_all_main_urls_and_templates_accessibility(self):

        self.client.login(username="admin_boss", password="securepassword123")

        endpoints = [
            ("manager:project-list", "manager/project_list.html"),
            ("manager:task-list", "manager/task_list.html"),
            ("manager:worker-list", "manager/worker_list.html"),
            ("manager:team-list", "manager/team_list.html"),
        ]

        for url_name, template_name in endpoints:
            with self.subTest(url=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Сторінка {url_name} повинна повертати статус 200"
                )
                self.assertTemplateUsed(
                    response,
                    template_name,
                    f"Сторінка {url_name} використовує неправильний шаблон"
                )

    def test_unauthenticated_user_redirect(self):
        response = self.client.get(reverse("manager:worker-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)