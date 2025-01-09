from django.urls import path

from myauth.views import (
    login_view,
    CustomLoginView,
)


app_name = "myauth"


urlpatterns = [
    # path("login/", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("custom_login/", CustomLoginView.as_view(), name="custom_login"),
]
