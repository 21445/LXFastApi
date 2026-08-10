
from tortoise import fields,models,Tortoise,run_async

class student(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    profile = fields.OneToOneField(
        "models.studentProfile", 
        on_delete=fields.CASCADE, 
        related_name="student",null=True)

class studentProfile(models.Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255)

class Grade(models.Model):
    id = fields.IntField(pk=True)
    score = fields.FloatField(max_length=20)
    student = fields.ForeignKeyField(
        "models.student", 
        on_delete=fields.CASCADE, 
        related_name="grades")

class Course(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    # students = fields.ManyToManyFieldField(
    #     "models.student", 
    #     through="models.Grade", 
    #     related_name="courses",
    #     through_fields="student_course"
    #     )

class StudentCourse(models.Model):
    id = fields.IntField(pk=True)
    student = fields.ForeignKeyField(
        "models.student", 
        on_delete=fields.CASCADE, 
        related_name="Course")
    course = fields.ForeignKeyField(
        "models.Course", 
        on_delete=fields.CASCADE, 
        related_name="students")
    class Meta:
        unique_together = ("student", "course")

async def init():
    await Tortoise.init(
        db_url="mysql://root:root@127.0.0.1:3307/fastapi_db4",
        modules={"models": ["model23"]},
        
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
