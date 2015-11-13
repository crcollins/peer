"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

import account

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/', include("account.urls")),
]

urlpatterns += patterns('django.contrib.auth.views',
    url(r"^login/$", "login", name="login"),
    url(r"^logout/$", "logout", name="logout"),
    url(r'^reset/$', 'password_reset', name="password_reset"),
    url(r'^reset/sent/$', 'password_reset_done', name="password_reset_done"),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    'password_reset_confirm'),
    url(r'^reset/done/$', 'password_reset_complete'),
)

urlpatterns += patterns('account.views',
    url(r"^register/$", "register_user", name="register"),
    url(r"^register/(?P<activation_key>[a-f0-9]*)$", "activate_user", name="activate"),
)
