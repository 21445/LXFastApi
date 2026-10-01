from tortoise.models import Model
from tortoise.fields import CharField, DatetimeField, BooleanField

class User(Model):
    id = CharField(max_length=36, pk=True)  # 主键，UUID 字符串
    username = CharField(max_length=50, unique=True)  # 用户名，唯一
    email = CharField(max_length=255, unique=True)  # 邮箱，唯一
    is_active = BooleanField(default=True)  # 是否激活
    created_at = DatetimeField(auto_now_add=True)  # 创建时间
    updated_at = DatetimeField(auto_now=True)  # 更新时间

    class Meta:
        table = "users"  # 自定义表名
        ordering = ["-created_at"]  # 默认按创建时间降序排序

    def __str__(self):
        return self.username