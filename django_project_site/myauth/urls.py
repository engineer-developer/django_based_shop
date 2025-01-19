from django.urls import path

from myauth.views import (
    login_view,
    CustomLoginView,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    logout_view,
    CustomLogoutView,
    AboutMeView,
    RegistrationView,
    not_authorized_view,
    FooBarView,
    ProfileUpdateView,
    ProfileCreateView,
    UsersListView,
)


app_name = "myauth"


urlpatterns = [
    # path("login/", login_view, name="login"),
    path("login/", CustomLoginView.as_view(), name="login"),
    # path("logout/", logout_view, name="logout"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about_me"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("session/set/", set_session_view, name="session_set"),
    path("session/get/", get_session_view, name="session_get"),
    path("not-authorized/", not_authorized_view, name="not_authorized"),
    path("foo-bar/", FooBarView.as_view(), name="foo_bar"),
    path("profile/create/", ProfileCreateView.as_view(), name="profile_create"),
    path(
        "profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile_update"
    ),
    path("users/", UsersListView.as_view(), name="users_list"),
]
