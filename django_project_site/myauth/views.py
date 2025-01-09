from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView


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
        return redirect("/admin/")

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
