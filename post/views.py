from math import ceil

from django.shortcuts import render, redirect

from post.models import Post
from post.helper import page_cache
from post.helper import rds


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create_post.html')


@page_cache(15)
def read_post(request):
    post_id = int(request.GET.get('post_id', 0))
    post = Post.objects.get(id=post_id)
    rds.zincrby('ReadRank', post_id)  # 记录阅读量到 redis
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
