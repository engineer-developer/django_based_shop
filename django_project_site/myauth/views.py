from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy

from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


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
    next_page = "/admin/"


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


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    """Set cookie"""

    response = HttpResponse("Cookie set")
    response.set_cookie(key="fizz", value="buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """Get cookie"""

    key = "fizz"
    value = request.COOKIES.get(key, "default value")
    return HttpResponse(f"Cookie with key {key!r} has value {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    """Set session"""

    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    """Get session"""

    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")
