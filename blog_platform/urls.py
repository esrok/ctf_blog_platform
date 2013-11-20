from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'blog_platform.views.display_latest_posts'),
    url(r'^latest/$', 'blog_platform.views.display_latest_posts'),
    url(r'^latest/(?P<count>\d+)/$', 'blog_platform.views.display_latest_posts'),
    url(r'^my/$', 'blog_platform.views.display_user_posts'),
    url(r'^write-post/$', 'blog_platform.views.write_post'),
    url(r'^accounts/register/$', 'blog_platform.views.register'),
    url(r'^accounts/login/$', 'blog_platform.views.login'),
    url(r'^accounts/logout/$', 'blog_platform.views.logout'),
    url(r'^(?P<author>\w{1,32})/(?P<slug>\w{1,40}/$)', 'blog_platform.views.display_blogpost')
)
