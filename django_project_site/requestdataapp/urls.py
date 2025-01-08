from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from requestdataapp.views import process_get_view, user_form, handle_file_upload


app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="user-form"),
    path("upload/", handle_file_upload, name="file-upload"),
]
