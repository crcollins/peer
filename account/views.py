import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from project.settings import HOME_URL
from account.forms import RegistrationForm, SettingsForm

import utils
import models

logger = logging.getLogger(__name__)


def register_user(request):
    if request.user.is_authenticated():
        return redirect(HOME_URL)

    state = "Please register"

    reg_form = RegistrationForm(request.POST or None)
    pass_form = SetPasswordForm(request.user, request.POST or None)
    temp1 = reg_form.is_valid()     # prevent short circuit
    temp2 = pass_form.is_valid()    # prevent short circuit
    if temp1 and temp2:
        d = dict(
            reg_form.cleaned_data.items() + pass_form.cleaned_data.items()
        )

        new_user = get_user_model().objects.create_user(d["username"],
                                            d["email"],
                                            d["new_password1"])
        new_user.is_active = False
        activation_key = models.ActivationKey(user=new_user)

        new_user.save()
        activation_key.save()

        logger.info("New user '%s' registered." % new_user.username)
        c = {
            "key": activation_key.value,
        }
        return render(request, "account/post_register.html", c)

    c = {
        "state": state,
        "reg_form": reg_form,
        "pass_form": pass_form,
    }
    return render(request, "account/register.html", c)


def activate_user(request, activation_key):
    user = get_object_or_404(get_user_model(), activationkey__value=activation_key)
    if not user.is_active:
        user.is_active = True
        user.save()
        logger.info("User '%s' activated." % user.username)
        return render(request, "account/activate.html")
    else:
        return redirect(HOME_URL)


@login_required
def account_page(request, username, page):
    if request.user.username != username:
        return redirect(account_page, request.user.username, page)
    return utils.PAGES[page](request, username)


@login_required
def user_settings(request, username):
    return redirect(account_page, request.user.username, "settings")


@login_required
@utils.add_account_page("settings")
def main_settings(request, username):
    state = "Change Settings"

    changed = False
    initial = {
        "email": request.user.email,
    }
    settings_form = SettingsForm(request.POST or None, initial=initial)
    if settings_form.is_valid():
        d = dict(settings_form.cleaned_data)
        if request.user.email != d.get("email"):
            request.user.email = d.get("email")
            logger.info("User '%s' updated email to %s." % (request.user.username, request.user.email))
            changed = True

    if changed:
        request.user.save()
        initial = {
            "email": request.user.email,
        }
        settings_form = SettingsForm(initial=initial)
        state = "Settings Successfully Saved"

    c = {
        "pages": utils.PAGES,
        "page": "settings",
        "state": state,
        "form": settings_form,
    }
    return render(request, "account/main_settings.html", c)


@login_required
@utils.add_account_page("password")
def password_settings(request, username):
    state = "Change Settings"

    changed = False
    pass_form = PasswordChangeForm(request.user, request.POST or None)
    if pass_form.is_valid():
        d = dict(pass_form.cleaned_data)
        if d.get("new_password1"):
            request.user.set_password(d.get("new_password1"))
            changed = True

    if changed:
        request.user.save()
        logger.info("User '%s' updated their password." % username)
        state = "Settings Successfully Saved"

    c = {
        "pages": utils.PAGES,
        "page": "password",
        "state": state,
        "form": pass_form,
    }
    return render(request, "account/password_settings.html", c)
