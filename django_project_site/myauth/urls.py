from django.urls import path

from myauth.views import (
    login_view,
    CustomLoginView,
    set_cookie_view,
    get_cookie_view,
)


app_name = "myauth"


urlpatterns = [
    # path("login/", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("custom_login/", CustomLoginView.as_view(), name="custom_login"),
    path("set_cookie/", set_cookie_view, name="set_cookie"),
    path("get_cookie/", get_cookie_view, name="get_cookie"),
]
