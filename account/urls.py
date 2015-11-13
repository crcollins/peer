from django.conf.urls import patterns, url


urlpatterns = patterns('account.views',
                        url(r'^(?P<username>[\w.@+-]+)/$',
                           "user_settings",
                           name="user_settings"),
                       )

# @add_account_page pages
urlpatterns += patterns('account.views',
                        url(r'^(?P<username>[\w.@+-]+)/(?P<page>[\w.@+-]+)/$',
                            "account_page",
                            name="account_page"),
                        )


