from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.views.generic import View
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V, F, Case, When, Func, Prefetch, Count
from django.conf import settings
from website.models import Blog, Tag, BlogTag
from website.forms import BlogForm
import traceback

class BlogView(View):
    '''
        블로그 리스트
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        blog_tag_list = Tag.objects.annotate(
            tag_count = Count("blog_tag", distinct=True)
        ).filter(tag_count__gt=0).order_by('-tag_count', 'name').values('name', 'tag_count')
        context['blog_tag_list'] = blog_tag_list
        context['blog_total_count'] = Blog.objects.all().count()
        
        filter_dict = {}
        paginate_by = '10'
        page = request.GET.get('page', '1')

        search = request.GET.get('search', '')
        context['search'] = search
        if search:
            filter_dict['title__icontains'] = search

        tag = request.GET.get('tag', None)
        context['tag'] = tag
        if tag:
            tag_obj = get_object_or_404(Tag, name=tag)
            filter_dict['id__in'] = list(BlogTag.objects.filter(tag=tag_obj).values_list('blog', flat=True))


        obj_list = Blog.objects.filter(**filter_dict).annotate(
            imageUrl=Case(
                When(image='', then=None),
                When(image=None, then=None),
                default=Concat(V(settings.SITE_URL), V(settings.MEDIA_URL), 'image', output_field=CharField())
            ),
            username=Case(
                When(user=None, then=V('None')),
                default=F('user__username'), output_field=CharField()
            ),
            createdAt=Func(
                F('created_at'),
                V('%y.%m.%d'),
                function='DATE_FORMAT',
                output_field=CharField()
            )
        ).values(
            'id',
            'title',
            'imageUrl',
            'username',
            'content',
            'createdAt'
        ).order_by('-id')

        if search:
            context['search_count'] = obj_list.count()


        paginator = Paginator(obj_list, paginate_by)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = 1
            page_obj = paginator.page(page)
        except InvalidPage:
            page = 1
            page_obj = paginator.page(page)

        for i in page_obj:
            i['tags'] = list(BlogTag.objects.filter(blog_id=i['id']).order_by('id').values_list('tag__name', flat=True))

        pagelist = paginator.get_elided_page_range(page, on_each_side=3, on_ends=1)
        context['pagelist'] = pagelist
        context['page_obj'] = page_obj
        
        return render(request,'blog/blog.html', context)
    

class BlogCreateView(View):
    '''
        블로그 작성
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['form'] = BlogForm
        user = request.user
        if not user.is_authenticated:
            next_url = request.get_full_path()
            return redirect(f"{resolve_url('website:login')}?next={next_url}")
        if not user.is_superuser:
            Http404('You do not have permission')

        return render(request,'blog/blog_create.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"message": "Login Please"}, status=401)
        if not user.is_superuser:
            return JsonResponse({"message": "You do not have permission"}, status=403)

        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        image = request.FILES.get('image')
        tags = request.POST['tags']
        tag_list = tags.split(',')
        tag_list = [i.strip() for i in tag_list]

        try:
            with transaction.atomic():
                blog = Blog.objects.create(
                    title=title,
                    content=content,
                    image=image,
                    user=request.user
                )
                for i in tag_list:
                    obj, created = Tag.objects.get_or_create(name=i)
                    BlogTag.objects.create(blog=blog, tag=obj)

        except:
            print(traceback.format_exc())

            return JsonResponse({"message": "Blog Posting Error"}, status=400)
        
        return JsonResponse({"url":reverse('website:blog')}, status=201)
    

class BlogDetailView(View):
    '''
        블로그 상세
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        pk = kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        context['blog'] = blog
        blog_tag_list = Tag.objects.annotate(
            tag_count = Count("blog_tag", distinct=True)
        ).filter(tag_count__gt=0).order_by('-tag_count', 'name').values('name', 'tag_count')
        context['blog_tag_list'] = blog_tag_list
        context['blog_total_count'] = Blog.objects.all().count()


        return render(request,'blog/blog_detail.html', context)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        try:
            blog = Blog.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Blog Id Error"}, status=400)
        
        if not user.is_authenticated:
            return JsonResponse({"message": "Login Please"}, status=401)
        if not user.is_superuser or blog.user != user:
            return JsonResponse({"message": "You do not have permission"}, status=403)
        
        blog.delete()
        return JsonResponse({"url":reverse('website:blog')}, status=201)
    

class BlogEditView(View):
    '''
        블로그 수정
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        pk = kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        context["blog"] = blog
        
        user = request.user
        if not user.is_authenticated:
            next_url = request.get_full_path()
            return redirect(f"{resolve_url('website:login')}?next={next_url}")
        if not user.is_superuser or blog.user != user:
            Http404('You do not have permission')

        context['form'] = BlogForm(instance=blog)
        tags = ''
        for i in blog.blog_tag.all():
            tags += f'{i.tag.name}, '
        tags = tags.strip().rstrip(',')
        context['tags'] = tags

        return render(request,'blog/blog_edit.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        try:
            blog = Blog.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Blog Id Error"}, status=400)

        if not user.is_authenticated:
            return JsonResponse({"message": "Login Please"}, status=401)
        if not user.is_superuser or blog.user != user:
            return JsonResponse({"message": "You do not have permission"}, status=403)
        
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        image = request.FILES.get('image')
        tags = request.POST['tags']
        tag_list = tags.split(',')
        tag_list = [i.strip() for i in tag_list]

        tag_id_list = list(BlogTag.objects.filter(blog=blog).values_list('pk', flat=True))
        try:
            with transaction.atomic():
                blog.title = title
                blog.content = content
                if image:
                    blog.image =image
                blog.save()
                new_tag_id_list = []
                for i in tag_list:
                    obj1, created1 = Tag.objects.get_or_create(name=i)
                    obj2, created2 = BlogTag.objects.get_or_create(blog=blog, tag=obj1)
                    new_tag_id_list.append(obj2.pk)
                # 차집합 제거..
                complement = list(set(tag_id_list) - set(new_tag_id_list))
                BlogTag.objects.filter(id__in=complement).delete()
        except:
            return JsonResponse({"message": "Blog Edit Error"}, status=400)
        
        return JsonResponse({"url":reverse('website:blog_detail', kwargs={'pk':blog.pk})}, status=202)