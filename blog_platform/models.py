from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class BlogPost(models.Model):
    title = models.CharField(max_length=40, blank=False, null=False)
    text = models.TextField(blank=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    private = models.BooleanField(default=False)

    creation_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_platform.views.display_blogpost', args=(self.author, self.slug))

    class Meta:
        verbose_name = _('BlogPost')
        verbose_name_plural = _('BlogPosts')
    