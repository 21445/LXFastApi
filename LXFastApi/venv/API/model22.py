
from tortoise import fields,models,Tortoise,run_async

class student(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    profile = fields.OneToOneField(
        "models.studentProfile", 
        on_delete=fields.CASCADE, 
        related_name="student")

class studentProfile(models.Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255)

async def init():
    await Tortoise.init(
        db_url="mysql://root:root@127.0.0.1:3307/fastapi_db4",
        modules={"models": ["model22"]},
        
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init())
