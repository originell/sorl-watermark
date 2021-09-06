"""Django settings for tests."""
from os.path import join as pjoin, abspath, dirname, pardir

from .base import FIXTURES_DIR

SECRET_KEY = "SECRET"
PROJ_ROOT = abspath(pjoin(dirname(__file__), pardir))

THUMBNAIL_PREFIX = "test/cache/"
THUMBNAIL_DEBUG = True
THUMBNAIL_LOG_HANDLER = {
    "class": "sorl.thumbnail.log.ThumbnailLogHandler",
    "level": "ERROR",
}
THUMBNAIL_KVSTORE = "watermark_tests_app.kvstore.TestKVStore"
THUMBNAIL_STORAGE = "watermark_tests_app.storage.TestStorage"
THUMBNAIL_VIPSTHUMBNAIL = "vipsthumbnail"
THUMBNAIL_VIPSHEADER = "vipsheader"
THUMBNAIL_REDIS_SSL = False
THUMBNAIL_WATERMARK = "mark.png"

DEFAULT_FILE_STORAGE = "watermark_tests_app.storage.TestStorage"
ADMINS = (("Sorl Watermark", "foobar@example.com"),)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
# FORGIVE ME: ugly, but django wants referenced files to live there
MEDIA_ROOT = pjoin(PROJ_ROOT, "tests", "fixtures")
MEDIA_URL = "/media/"
ROOT_URLCONF = "tests.thumbnail_tests.urls"
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "sorl.thumbnail",
    "tests.watermark_tests_app",
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]
MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATICFILES_DIRS = [
    FIXTURES_DIR,
]
