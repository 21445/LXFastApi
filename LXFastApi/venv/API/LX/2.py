from getpass import getuser
from re import U

from fastapi import FastAPI

app = FastAPI()

from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tortoise-ORM 配置
TORTOISE_ORM: Dict = {
    "connections": {
        # 开发环境使用 SQLite（基于文件，无需服务器）
        #"default": "sqlite://db.sqlite3",
        # 生产环境示例：PostgreSQL
        # "default": "postgres://user:password@localhost:5432/dbname",
        # 生产环境示例：MySQL
        "default": "mysql://root:root@127.0.0.1:3306/suatibao",
    },
    "apps": {
        "models": {
            "models": ["ShuTiBao", "aerich.models"],  # 模型模块和 Aerich 迁移模型
            
            "default_connection": "default",
        }
    },
    # 连接池配置（推荐）
    "use_tz": False,  # 是否使用时区
    "timezone": "UTC",  # 默认时区
    "db_pool": {
        "max_size": 10,  # 最大连接数
        "min_size": 1,   # 最小连接数
        "idle_timeout": 30  # 空闲连接超时（秒）
    }
}

from tortoise.contrib.fastapi import register_tortoise

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True,)  # 注册 Tortoise-ORM 到 FastAPI 应用，生成数据库模式并添加异常处理程序

# from data_stu import create_users
from ShuTiBao import users
from ShuTiBao import submissions,computer_quiz


# @app.get("/")
# async def read_root():
#   usde = await create_users("12345556", "testuser111", "test@example.com")
#   return usde

@app.get("/user")
async def read_root():
  usder = await users.all().limit(2).offset(0)
  print(usder)
  return usder

@app.get("/getquestion")
async def read_root( id:str ):
    getuser = await computer_quiz.filter(question_id=id).first()
    print(getuser)
    aaa = await submissions.filter(question_id=id)
    return getuser,aaa

@app.get("/getusers")
async def read_root(id:int ):
    getuser = await users.get(id=id)
    
    return getuser

@app.post("/getuser")
async def read_root(id:int ,name:str = None,emall:str = None ):
    getuser = await users.get(id=id)
    if name:
        getuser.username = name
    if emall is not None:
        getuser.email = emall
    await getuser.save()
    return getuser


@app.get("/deluser")
async def read_root(id:int ):
    delluser = await users.get(id=id)
    await delluser.delete()
    return delluser
    # return {"message": "User deleted successfully"}


if __name__ == "__main__":  # 当直接运行此脚本时（而非作为模块导入时）
    import uvicorn  # 导入uvicorn ASGI服务器
    uvicorn.run("2:app", host="0.0.0.0", port=8000, reload=True)  # 启动FastAPI应用，监听所有网络接口的8000端口

