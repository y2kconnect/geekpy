from math import ceil

from django.shortcuts import render, redirect
from django.core.cache import cache

from post.models import Post


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create_post.html')


def read_post(request):
    post_id = int(request.GET.get('post_id', 0))

    key = 'Post-%s' % post_id
    post = cache.get(key)  # 首先检查缓存
    if post is None:
        print('get post %s from db' % post_id)
        post = Post.objects.get(id=post_id)
        cache.set(key, post, 86400)

    return render(request, 'read_post.html', {'post': post})


def edit_post(request):
    if request.method == 'POST':
        # 获取提交参数
        post_id = int(request.POST.get('post_id', 0))
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.get(id=post_id)
        # 修改文章内容
        post.title = title
        post.content = content
        post.save()
        # 修改缓存
        key = 'Post-%s' % post_id
        cache.set(key, post, 86400)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id', 0))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})


def post_list(request):
    page = int(request.GET.get('page', 1))
    pages = ceil(Post.objects.count() / 5)

    # start = (page - 1) * 5
    # end = page * 5
    # posts = Post.objects.filter(id__gt=start, id__lte=end)
    # return render(request, 'post_list.html',
    #               {'posts': posts, 'pages': range(1, pages + 1)})

    start = (page - 1) * 5
    end = page * 5
    posts = Post.objects.all()[start:end]
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(1, pages + 1)})
