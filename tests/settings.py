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
THUMBNAIL_KVSTORE = "tests.thumbnail_tests.kvstore.TestKVStore"
THUMBNAIL_STORAGE = "tests.thumbnail_tests.storage.TestStorage"
DEFAULT_FILE_STORAGE = "tests.thumbnail_tests.storage.TestStorage"
ADMINS = (("Sorl Watermark", "foobar@example.com"),)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
MEDIA_ROOT = pjoin(PROJ_ROOT, "media")
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
THUMBNAIL_REDIS_SSL = False

STATICFILES_DIRS = [FIXTURES_DIR,]
THUMBNAIL_WATERMARK = "mark.png"
