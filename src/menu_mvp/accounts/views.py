from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from menu_mvp.accounts.forms import SignupForm


class HomeView(TemplateView):
    template_name = "home.html"


class LoginPageView(LoginView):
    template_name = "accounts/login.html"


class LogoutPageView(LogoutView):
    next_page = reverse_lazy("home")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})
