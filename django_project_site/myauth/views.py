from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
from django.urls import reverse, reverse_lazy

from .models import Profile
from .forms import ProfileForm, AboutMeAvatarUpdateForm


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class AboutMeAvatarUpdateView(UpdateView):
    template_name = "myauth/about-avatar-update.html"
    model = Profile
    form_class = AboutMeAvatarUpdateForm
    success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form):
        response = super().form_valid(form)
        image = form.files.get("avatar")
        profile = form.instance
        profile.avatar = image
        profile.save()
        return response


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    """Implement login view"""

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")
        return render(request, "myauth/login.html")

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse("myauth:about_me"))

    return render(
        request,
        "myauth/login.html",
        context={"error": "Invalid login credentials"},
    )


class CustomLoginView(LoginView):
    """Implement login view via class-based view"""

    template_name = "myauth/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("myauth:about_me")


def logout_view(request: HttpRequest) -> HttpResponse:
    """Implement logout view"""

    logout(request)
    return redirect(reverse("myauth:login"))


class CustomLogoutView(LogoutView):
    """Implement logout view via class-based view"""

    http_method_names = ["get"]
    next_page = reverse_lazy("myauth:login")

    def get(self, request, *args, **kwargs):
        """Logout may be done via GET."""
        logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)


def check_is_superuser(user):
    """Function to check if user is superuser"""

    return True if user.is_superuser else False


@user_passes_test(test_func=check_is_superuser, login_url="/myauth/not-authorized/")
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    """Set cookie

    Decorator "user_passes_test" checks that user is superuser.
    """

    response = HttpResponse("Cookie set")
    response.set_cookie(key="fizz", value="buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """Get cookie"""

    key = "fizz"
    value = request.COOKIES.get(key, "default value")
    return HttpResponse(f"Cookie with key {key!r} has value {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    """Set session

    Decorator "permission_required" checks that user have permission to view profile.
    """

    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    """Get session

    Decorator "login_required" checks that user is logged in.
    """

    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


def not_authorized_view(request: HttpRequest) -> HttpResponse:
    """Not authorized view"""

    return render(request, "myauth/not_authorized.html")


class FooBarView(View):
    def get(self, request) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


class ProfileCreateView(CreateView):
    model = Profile
    fields = "bio", "agreement_accepted", "avatar"
    template_name = "myauth/profile_form.html"
    success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        profile = self.get_object()
        checking_conditions = (self.request.user.pk == profile.user.pk,)
        # return self.request.user.is_superuser or all(checking_conditions)
        return True

    model = Profile
    form_class = ProfileForm
    template_name_suffix = "_update_form"
    context_object_name = "profile"

    def get_success_url(self):
        return reverse(
            "myauth:user_details",
            kwargs={"pk": self.object.user.pk},
        )


class UsersListView(ListView):
    template_name = "myauth/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.select_related("profile")


class UserDetailsView(DetailView):
    template_name = "myauth/user_details.html"
    context_object_name = "user"

    def get_queryset(self):
        return User.objects.select_related("profile")
