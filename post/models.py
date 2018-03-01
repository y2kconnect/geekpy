from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            # 将 _auth 缓存为 self 的属性 (对象级别缓存)
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def get_comments(self):
        return Comment.objects.filter(pid=self.id)

    def get_tags(self):
        pt_list = PostTag.objects.filter(pid=self.id).only('tid')
        tid_list = [pt.tid for pt in pt_list]
        return Tag.objects.filter(id__in=tid_list)

    def update_tags(self, tag_names):
        need_delete_tid_list = []

        tag_names = set(t.capitalize() for t in tag_names)
        tags = self.get_tags()
        for tag in tags:
            if tag.name not in tag_names:
                need_delete_tid_list.append(tag.id)
            else:
                # 剔除不需要处理的 Tag
                tag_names.remove(tag.name)
        # 从数据库删除不再需要的 Tag
        PostTag.objects.filter(pid=self.id, tid__in=need_delete_tid_list).delete()

        # 对已有的 Tag 创建关系
        for t in Tag.objects.filter(name__in=tag_names):
            PostTag.objects.create(pid=self.id, tid=t.id)
            tag_names.remove(t.name)

        # 创建新的 Tags
        Tag.objects.bulk_create([Tag(name=n) for n in tag_names])
        new_tags = Tag.objects.filter(name__in=tag_names)

        # 创建新的关系
        new_post_tags = [PostTag(pid=self.id, tid=t.id) for t in new_tags]
        PostTag.objects.bulk_create(new_post_tags)


class Comment(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=128, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.pid)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True, blank=False, null=False)

    def get_posts(self):
        pt_list = PostTag.objects.filter(tid=self.id).only('pid')
        pid_list = [pt.pid for pt in pt_list]
        return Post.objects.filter(id__in=pid_list)


class PostTag(models.Model):
    pid = models.IntegerField()
    tid = models.IntegerField()
