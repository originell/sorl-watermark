from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from .views import direct_to_template

urlpatterns = [
    re_path(
        r"^media/(?P<path>.+)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    re_path(r"^(.*\.html)$", direct_to_template),
]
