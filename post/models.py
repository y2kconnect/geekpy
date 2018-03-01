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


class Comment(models.Model):
    pass
