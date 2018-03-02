from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    nickname = models.CharField(max_length=64, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()

    def verify_password(self, password):
        return check_password(password, self.password)

    def add_perm(self, perm_name):
        '''增加权限'''
        try:
            perm = Permission.objects.get(name=perm_name)
        except Permission.DoesNotExist as e:
            return e
        Role.objects.get_or_create(uid=self.id, perm_id=perm.id)

    def del_perm(self, perm_name):
        '''取消权限'''
        try:
            perm = Permission.objects.get(name=perm_name)
            Role.objects.get(uid=self.id, perm_id=perm.id).delete()
        except (Permission.DoesNotExist, Role.DoesNotExist) as e:
            print(e)

    def has_perm(self, perm_name):
        '''权限检查'''
        perm = Permission.objects.get(name=perm_name)
        return Role.objects.filter(uid=self.id, perm_id=perm.id).exists()

    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()


class Permission(models.Model):
    '''权限'''
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)


class Role(models.Model):
    '''
        角色表
        ID    用户  权限
        ----------------
         1     A    产品
         2     D    开发者
         3     C    财务
         4     M    产品
         5     M    开发者
         6     B    产品
         7     B    开发者
         8     B    财务
         9     D    产品
    '''
    uid = models.IntegerField()
    perm_id = models.IntegerField()
