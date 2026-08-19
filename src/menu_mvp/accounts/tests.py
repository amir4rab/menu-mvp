from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


def logged_in_user_id(client):
    session = client.session
    user_id = session.get(SESSION_KEY)
    return int(user_id) if user_id is not None else None


class SignupTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {"username": "alice", "password1": "correct-horse-1", "password2": "correct-horse-1"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="alice").exists())
        self.assertEqual(logged_in_user_id(self.client), User.objects.get(username="alice").pk)

    def test_signup_requires_unique_username(self):
        User.objects.create_user(username="alice", password="correct-horse-1")
        response = self.client.post(
            reverse("accounts:signup"),
            {"username": "alice", "password1": "correct-horse-1", "password2": "correct-horse-1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")
        self.assertIsNone(logged_in_user_id(self.client))

    def test_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {"username": "alice", "password1": "correct-horse-1", "password2": "different-pass-2"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "didn")
        self.assertFalse(User.objects.filter(username="alice").exists())

    def test_signup_rejects_common_password(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {"username": "alice", "password1": "password", "password2": "password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "too common")
        self.assertFalse(User.objects.filter(username="alice").exists())

    def test_signup_renders_form_for_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="correct-horse-1")

    def test_login_with_valid_credentials_redirects(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alice", "password": "correct-horse-1"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(logged_in_user_id(self.client), self.user.pk)

    def test_login_respects_next_parameter(self):
        response = self.client.post(
            reverse("accounts:login") + "?next=/some/private/page/",
            {"username": "alice", "password": "correct-horse-1"},
        )
        self.assertRedirects(response, "/some/private/page/", fetch_redirect_response=False)

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alice", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "correct username and password")
        self.assertIsNone(logged_in_user_id(self.client))

    def test_login_rejects_unknown_username(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "nobody", "password": "correct-horse-1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "correct username and password")
        self.assertIsNone(logged_in_user_id(self.client))

    def test_login_requires_post(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(logged_in_user_id(self.client))


class LogoutTests(TestCase):
    def test_logout_requires_post_and_redirects(self):
        self.client.force_login(User.objects.create_user(username="alice", password="correct-horse-1"))
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertIsNone(logged_in_user_id(self.client))

    def test_logout_get_is_not_allowed(self):
        self.client.force_login(User.objects.create_user(username="alice", password="correct-horse-1"))
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)


class HomePageTests(TestCase):
    def test_home_page_is_public(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_shows_username_when_logged_in(self):
        user = User.objects.create_user(username="alice", password="correct-horse-1")
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "alice")