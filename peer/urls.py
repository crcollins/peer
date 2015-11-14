from django.conf.urls import include, url, patterns


urlpatterns = patterns('peer.views',
    url(r'^$', 'index', name="index"),
    url(r'^browse/$', 'paper_index', name="paper_index"),
    url(r'^browse/(?P<paper_id>\d+)/$', 'paper_detail', name="paper_detail"),
    url(r'^submit/$', 'paper_submit', name="paper_submit"),
    url(r'^submission/$', 'submission_index', name="submission_index"),
    url(r'^submission/(?P<paper_id>\d+)/$', 'submission_detail', name="submission_detail"),
)


