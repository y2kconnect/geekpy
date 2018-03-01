from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    nickname = models.CharField(max_length=64, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()
    perm = models.IntegerField(default=0)

    def verify_password(self, password):
        return check_password(password, self.password)

    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()
