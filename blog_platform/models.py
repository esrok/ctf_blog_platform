from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class BlogPost(models.Model):
    TITLE_LENGTH = 40
    TEXT_PREVIEW_LENGTH = 100
    PREVIEW_SUFFIX = '...'

    title = models.CharField(max_length=TITLE_LENGTH, blank=False, null=False)
    slug = models.SlugField(max_length=TITLE_LENGTH)
    text = models.TextField(blank=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    private = models.BooleanField(default=False)

    creation_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    @property
    def text_preview(self):
        if len(self.text) <= self.TEXT_PREVIEW_LENGTH:
            return self.text
        return self.text[:self.TEXT_PREVIEW_LENGTH - len(self.PREVIEW_SUFFIX)] + self.PREVIEW_SUFFIX

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_platform.views.display_post', args=(self.author, self.slug))

    class Meta:
        verbose_name = _('BlogPost')
        verbose_name_plural = _('BlogPosts')
