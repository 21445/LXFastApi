from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


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
        "default": "mysql://root:root@127.0.0.1:3306/shuatibao",
    },
    "apps": {
        "models": {
            "models": ["tortoise_models", "aerich.models"],  # 模型模块和 Aerich 迁移模型
            
            "default_connection": "default",
        }
    },
    # 连接池配置（推荐）
    "use_tz": False,  # 是否使用时区
    "timezone": "Asia/Shanghai",  # 默认时区
    "db_pool": {
        "max_size": 10,  # 最大连接数
        "min_size": 1,   # 最小连接数
        "idle_timeout": 30  # 空闲连接超时（秒）

    }
}
from tortoise.contrib.fastapi import register_tortoise
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True,)

from tortoise_models import User,UserAuth,UserBadge,UserMessage,SmsCode
from sms_login import send_email_code,verify_code
from register_login import register_token
from fastapi import Query



@app.post("/login")
async def read_user(
    phone: str = Query(..., description="请输入手机号"),
    password: str = Query(..., description="请输入登录密码")
):
    # 修复：get_or_none 不需要 .first()
    users = await User.get_or_none(phone=phone)
    if users is None:
        return {"code":400,"error": "还没有此用户，请注册用户"}

    if users.status == 0:
        return {"code":400,"error": "账号已封禁"}
    
    # 修复：通过用户关联查密码，不要单独按密码查！
    userauth = await UserAuth.get_or_none(user_id=users.id)
    if userauth is None or userauth.credential != password:
        return {"code":400,"error": "用户密码或手机号错误"}

    token = await register_token(phone,password)
    return {"code":200,"token":token}







from fastapi import Request

# 获取客户端IP工具
def get_client_ip(request: Request):
    return request.client.host

# 发送验证码接口
@app.get("/send_email_code")
async def api_send_code(request: Request, email: str, scene: str = "register"):
    ip = get_client_ip(request)
    code = await send_email_code(email, scene, ip)
    if code:
        return {"code":200,"msg":"发送成功"}
    return {"code":500,"msg":"发送失败"}

# 校验验证码接口
@app.post("/verify_email_code")
async def api_verify(email: str, scene: str, code: str):
    ok = await verify_code(email, scene, code)
    if ok:
        return {"code":200,"msg":"验证通过"}
    return {"code":400,"msg":"验证码错误/已过期/已使用"}


from register_login import register_user,register_auth

@app.get("/register")
async def read_user(phone:str,password:str,scene:str = "register"):
    users = await User.get_or_none(phone=phone).first()
    if users is not None:
        return {"error": "手机号已注册"}
    await register_user(phone,scene)
    auth = await UserAuth.get_or_none(identifier=phone).first()
    if auth is not None:

        return {"error": "用户已绑定"}
    else:
        await register_auth(phone,password)

 
    return {"code":200,"msg":"注册成功","auth":auth}
    

# @app.get("/gettoken")
# async def read_user(phone:str,password:str):
#     token = await register_token(phone,password)
#     return {"token":token}






if __name__ == "__main__":  # 当直接运行此脚本时（而非作为模块导入时）
    import uvicorn  # 导入uvicorn ASGI服务器
    uvicorn.run("ShuTiBao_api:app", host="0.0.0.0", port=8000, reload=True)  # 启动FastAPI应用，监听所有网络接口的8000端口
