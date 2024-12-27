from django.apps import AppConfig
from django.utils.functional import new_method_proxy


class RequestdataappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "requestdataapp"
