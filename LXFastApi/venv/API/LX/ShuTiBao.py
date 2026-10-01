from tortoise.models import Model
from tortoise.fields import IntField,CharField,DecimalField,TextField,DatetimeField,BooleanField

class users(Model):
    id = IntField(pk=True, generated=True)  # 主键，自增整数
    user_id = CharField(max_length=50, unique=True, null=True)  # 用户名，唯一
    username = CharField(max_length=50, unique=True)  # 用户名，唯一
    password_md5 = CharField(max_length=32, null=False)  # 密码，唯一
    email = CharField(max_length=255, unique=True)  # 邮箱，唯一
    phone = CharField(max_length=20, null=True)  # 手机号，唯一
    status = CharField(max_length=20, default='Active')  # 是否激活
    created_at = DatetimeField(auto_now_add=True)  # 创建时间
    # updated_at = DatetimeField(auto_now=True)  # 更新时间

    class Meta:
        table = "users"  # 自定义表名
        ordering = ["id"]  # 默认按创建时间升序排序

    def __str__(self):
        return self.username


class computer_quiz(Model):
    id = IntField(pk=True, generated=True)  # 自增主键
    question_id = CharField(max_length=50, unique=True, null=False)  # 题目编号 (如 Q1001)
    category = CharField(max_length=100, null=False)  # 学科分类
    difficulty = CharField(max_length=20, null=False)  # 难度 (Easy/Medium/Hard)
    title = TextField(null=False)  # 题干文本
    option_a = TextField(null=False)  # 选项 A
    option_b = TextField(null=False)  # 选项 B
    option_c = TextField(null=False)  # 选项 C
    option_d = TextField(null=False)  # 选项 D
    correct_answer = CharField(max_length=10, null=False)  # 正确选项 (A/B/C/D)
    explanation = TextField(null=True)  # 题目深度解析

    class Meta:
        table = "computer_quiz"
        ordering = ["id"]  # 默认按创建时间升序排序

    def __str__(self):
        return self.question_id

class submissions(Model):
    id = IntField(pk=True, generated=True)  # 主键，自增整数
    user_id = CharField(max_length=50, null=False)  # 用户ID (如 U1001)
    question_id = CharField(max_length=50, null=False)  # 题目ID (关联 questions.question_id)
    status = CharField(max_length=50, null=False)  # 状态 (Accepted, Wrong Answer, Runtime Error 等)
    language = CharField(max_length=30, null=False)  # 提交语言
    runtime_ms = IntField(default=0)  # 运行耗时 (毫秒)
    memory_mb = DecimalField(max_digits=5, decimal_places=1, default=0.0)  # 内存消耗 (MB)
    submitted_at = DatetimeField(null=False)  # 提交时间

    class Meta:
        table = "submissions"  # 自定义表名
        ordering = ["id"]  # 默认按创建时间升序排序

    def __str__(self):
        return self.question_id
  