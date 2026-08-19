from django.urls import path

from menu_mvp.accounts.views import LoginPageView, LogoutPageView, signup

app_name = "accounts"

urlpatterns = [
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
]
