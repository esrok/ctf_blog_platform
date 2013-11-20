from django.forms import ModelForm

from models import BlogPost

class WriteBlogPostForm(ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'private']