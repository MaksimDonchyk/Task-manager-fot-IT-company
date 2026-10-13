from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from manager.views import WorkerCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', WorkerCreateView.as_view(), name='register'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("manager.urls", namespace="manager")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
