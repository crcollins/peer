import os
from unittest import skipUnless

from django.test import Client, TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import views


def _register(client, data):
    response = client.post(reverse(views.register_user), data)
    assert response.status_code == 200
    content = response.content
    start = content.index("Please click")
    end = content.index("this", start) - 2
    url = content[start:end].split('href="')[1]
    key = url.split('register/')[1]
    response = client.get(reverse(views.activate_user, args=(key, )))
    assert response.status_code == 200
    v = client.login(username=data["username"], password=data["new_password1"])
    assert v
    client.logout()
    return key

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.users = [{
            "username": "user1",
            "email": "user1@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }, {
            "username": "user2",
            "email": "user2@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }]
        for user in self.users:
            new_user = get_user_model().objects.create_user(user["username"],
                                                user["email"],
                                                user["new_password1"])
            new_user.save()

    def test_register_page(self):
        response = self.client.get(reverse(views.register_user))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        data = {
            "username": "testman",
            "email": "testman@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }
        _register(self.client, data)

    def test_register_taken_username(self):
        data = {
            "username": "testman1",
            "email": "testman1@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }
        _register(self.client, data)
        self.assertRaises(ValueError, _register, self.client, data)

    def test_register_bad_password(self):
        data = {
            "username": "testmanpass",
            "email": "testmanpass@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass123",
        }
        self.assertRaises(ValueError, _register, self.client, data)

    def test_register_after_login(self):
        for user in self.users:
            r = self.client.login(
                username=user["username"],
                password=user["new_password1"])
            self.assertTrue(r)
            response = self.client.get(reverse(views.register_user))
            self.assertEqual(response.status_code, 302)

    def test_activation_page_after_activated(self):
        data = {
            "username": "testmankey",
            "email": "testmankey@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }
        key = _register(self.client, data)
        response = self.client.get(reverse(views.activate_user, args=(key, )))
        self.assertEqual(response.status_code, 302)


class SettingsTestCase(TestCase):
    users = [{
        "username": "vagrant",
        "email": "user1@test.com",
        "new_password1": "mypass",
        "new_password2": "mypass",
    }, {
        "username": "user2",
        "email": "user2@test.com",
        "new_password1": "mypass",
        "new_password2": "mypass",
    }]

    def setUp(self):
        self.client = Client()
        for user_info in self.users:
            new_user = get_user_model().objects.create_user(user_info["username"],
                                                user_info["email"],
                                                user_info["new_password1"])
            new_user.save()

    def test_settings_redirect_page(self):
        for user_info in self.users:
            r = self.client.login(
                username=user_info["username"],
                password=user_info["new_password1"])
            self.assertTrue(r)
            response = self.client.get(reverse(views.user_settings,
                                               args=(user_info["username"], )))
            self.assertEqual(response.status_code, 302)

    def test_change_settings_page(self):
        for user_info in self.users:
            r = self.client.login(
                username=user_info["username"],
                password=user_info["new_password1"])
            self.assertTrue(r)
            response = self.client.get(reverse(views.account_page,
                                               args=(user_info["username"],
                                                     "settings")))
            self.assertEqual(response.status_code, 200)

    def test_change_settings_redirect(self):
        for i, user_info in enumerate(self.users):
            r = self.client.login(
                username=user_info["username"],
                password=user_info["new_password1"])
            self.assertTrue(r)
            opposite = self.users[not i]["username"]
            response = self.client.get(reverse(views.account_page,
                                               args=(opposite, "settings")))
            self.assertEqual(response.status_code, 302)

    def test_change_email(self):
        for user_info in self.users:
            r = self.client.login(
                username=user_info["username"],
                password=user_info["new_password1"])
            self.assertTrue(r)

            response = self.client.get(reverse(views.account_page,
                                               args=(user_info["username"],
                                                     "settings")))
            self.assertEqual(response.status_code, 200)

            data = {"email": 'a' + user_info["email"]}
            response = self.client.post(reverse(views.account_page,
                                                args=(user_info["username"],
                                                      "settings")),
                                        data)
            self.assertIn("Settings Successfully Saved", response.content)

            user = get_user_model().objects.get(username=user_info["username"])
            self.assertEqual(user.email, 'a' + user_info["email"])
            user.email = user_info["email"]
            user.save()

    def test_change_password(self):
        for user_info in self.users:
            r = self.client.login(username=user_info["username"],
                                  password=user_info["new_password1"])
            self.assertTrue(r)

            response = self.client.get(reverse(views.account_page,
                                               args=(user_info["username"],
                                                     "password")))
            self.assertEqual(response.status_code, 200)
            data = {
                "old_password": user_info["new_password1"],
                "new_password1": user_info["new_password1"] + 'a',
                "new_password2": user_info["new_password2"] + 'a',
            }
            response = self.client.post(reverse(views.account_page,
                                                args=(user_info["username"],
                                                      "password")),
                                        data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Settings Successfully Saved", response.content)
            self.client.logout()

            r = self.client.login(username=user_info["username"],
                                  password=user_info["new_password1"] + 'a')
            self.assertTrue(r)
            user = get_user_model().objects.get(username=user_info["username"])
            user.set_password(user_info["new_password1"])

    def test_change_password_fail(self):
        for user_info in self.users:
            r = self.client.login(username=user_info["username"],
                                  password=user_info["new_password1"])
            self.assertTrue(r)

            response = self.client.get(reverse(views.account_page,
                                               args=(user_info["username"],
                                                     "password")))
            self.assertEqual(response.status_code, 200)
            data = {
                "old_password": user_info["new_password1"],
                "new_password1": user_info["new_password1"] + 'a',
                "new_password2": user_info["new_password2"],
            }
            self.assertNotIn("The two password fields", response.content)
            response = self.client.post(reverse(views.account_page,
                                                args=(user_info["username"],
                                                      "password")),
                                        data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("The two password fields", response.content)


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.users = [{
            "username": "user1",
            "email": "user1@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }, {
            "username": "user2",
            "email": "user2@test.com",
            "new_password1": "mypass",
            "new_password2": "mypass",
        }]
        for user in self.users:
            new_user = get_user_model().objects.create_user(user["username"],
                                                user["email"],
                                                user["new_password1"])
            new_user.save()

    def test_login(self):
        for user in self.users:
            response = self.client.get("/login/")
            self.assertEqual(response.status_code, 200)

            data = {
                "username": user["username"],
                "password": user["new_password1"],
            }
            response = self.client.post("/login/", data)
            self.assertEqual(response.status_code, 302)

    def test_invalid_username(self):
        for user in self.users:
            response = self.client.get("/login/")
            self.assertEqual(response.status_code, 200)

            data = {
                "username": user["username"] + 'a',
                "password": user["new_password1"],
            }
            response = self.client.post("/login/", data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("alert-danger", response.content)

    def test_invalid_password(self):
        for user in self.users:
            response = self.client.get("/login/")
            self.assertEqual(response.status_code, 200)

            data = {
                "username": user["username"],
                "password": user["new_password1"] + 'a',
            }
            response = self.client.post("/login/", data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("alert-danger", response.content)

    def test_logout(self):
        for user in self.users:
            r = self.client.login(username=user["username"],
                                  password=user["new_password1"])
            self.assertTrue(r)

            data = {
                "username": user["username"],
                "password": user["new_password1"],
            }
            response = self.client.get("/logout/", data)
            self.assertEqual(response.status_code, 200)

