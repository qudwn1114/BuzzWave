from django.conf import settings
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V, F, Case, When, Func, Prefetch, Count
from website.models import Blog

def global_variables(request):
    context={}
    recent_post = Blog.objects.all().annotate(
            imageUrl=Case(
                When(image='', then=None),
                When(image=None, then=None),
                default=Concat(V(settings.SITE_URL), V(settings.MEDIA_URL), 'image', output_field=CharField())
            ),
            createdAt=Func(
                F('created_at'),
                V('%d %M'),
                function='DATE_FORMAT',
                output_field=CharField()
            )
        ).values(
            'id',
            'title',
            'imageUrl',
            'createdAt'
        ).order_by('-id')[:2]
    
    context['recent_post'] = recent_post

    return context