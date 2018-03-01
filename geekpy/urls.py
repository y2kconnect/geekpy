"""geekpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from post import views as post_views
from user import views as user_views

urlpatterns = [
    path('', post_views.post_list),

    # 文章
    path('post/read/', post_views.read_post),
    path('post/create/', post_views.create_post),
    path('post/edit/', post_views.edit_post),
    path('post/list/', post_views.post_list),
    path('post/top10/', post_views.top10_posts),
    path('post/comment/', post_views.comment),
    path('post/tag/', post_views.tag_posts),

    # 用户
    path('user/register/', user_views.register),
    path('user/login/', user_views.login),
    path('user/logout/', user_views.logout),
    path('user/info/', user_views.user_info)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
