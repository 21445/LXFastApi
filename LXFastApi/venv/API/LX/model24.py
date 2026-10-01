from tortoise import Tortoise,run_async
from model23 import student,Course,studentProfile,Grade,StudentCourse

async def init():
    await Tortoise.init(
        db_url="mysql://root:root@127.0.0.1:3307/fastapi_db4",
        modules={"models": ["model23"]},
        )

async def create_data():
    await init()
    # 一对一关系
    stu1 = await student.create(name="吕布",)
    pro1 = await studentProfile.create(address="中国", phone="13800000000",)
    stu1.profile = pro1
    await stu1.save()

    pro2 = await studentProfile.create(address="日本", phone="13800000000")
    stu2 = await student.create(name="张三", profile=pro2)
    
    # 一对多关系
    stu3 = await student.create(name="李四", )
    await Grade.create(student=stu3,score=90,)
    await Grade.create(student=stu3,score=80)
    await Grade.create(student=stu3,score=70)

    #多对多关系
    stu4 = await student.create(name="王五", )
    stu5 = await student.create(name="赵六", )
    cou1 = await Course.create(name="python", )
    cou2 = await Course.create(name="java", )
    await StudentCourse.create(student=stu4,course=cou1)
    await StudentCourse.create(student=stu4,course=cou2)
    await StudentCourse.create(student=stu5,course=cou1)
    await StudentCourse.create(student=stu5,course=cou2)
    
async def updata_data():
    await init()
    upstu1 = await student.get(id=26)
    uppro1 = await studentProfile.get(id=7)
    upstu1.profile = uppro1
    await upstu1.save()
    


if __name__ == "__main__":
    run_async(updata_data())