from math import ceil

from django.shortcuts import render, redirect

from post.models import Post, Comment, Tag
from post.helper import page_cache
from post.helper import rds
from post.helper import get_post_rank
from user.helper import check_perm


@check_perm('user')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create_post.html')


@page_cache(1)
def read_post(request):
    post_id = int(request.GET.get('post_id', 0))
    post = Post.objects.get(id=post_id)
    rds.zincrby('ReadRank', post_id)  # 记录阅读量到 redis
    comments = post.get_comments()
    tags = post.get_tags()
    return render(request, 'read_post.html',
                  {'post': post, 'comments': comments, 'tags': tags})


@check_perm('user')
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
        # 设置文章的 Tags
        tags = request.POST.get('tags')
        tags = [t.strip() for t in tags.split(',')]
        post.update_tags(tags)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id', 0))
        post = Post.objects.get(id=post_id)
        tags = ', '.join(t.name for t in post.get_tags())
        return render(request, 'edit_post.html', {'post': post, 'tags': tags})


@check_perm('admin')
def delete_post(request):
    return render(request, 'delete_post.html')


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


def top10_posts(request):
    top10 = get_post_rank(10)
    return render(request, 'top10.html', {'top10': top10})


def comment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        Comment.objects.create(pid=post_id, name=name, content=content)
    return redirect('/post/read/?post_id=%s' % post_id)


def tag_posts(request):
    tag_id = int(request.GET.get('tag_id'))
    tag = Tag.objects.get(id=tag_id)
    posts = tag.get_posts()
    return render(request, 'post_list.html', {'posts': posts})
