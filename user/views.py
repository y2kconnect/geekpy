from django.shortcuts import render, redirect

from user.models import User
from user.forms import RegisterForm
from post.helper import page_cache


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist as e:
            return render(request, 'login.html', {'error': '用户不存在'})

        # 验证用户密码，并执行登陆操作
        if user.verify_password(password):
            request.session['uid'] = user.id  # 通过 session 保存用户状态
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'login.html', {'error': '用户名密码错误'})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            request.session['uid'] = user.id  # 通过 session 保存用户状态
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    else:
        return render(request, 'register.html')


@page_cache(10)
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})


def logout(request):
    request.session.flush()
    return redirect('/user/login/')
