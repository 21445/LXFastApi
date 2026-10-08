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
    email: str = Query(..., description="请输入邮箱"),
    password: str = Query(..., description="请输入登录密码")
):
    # 修复：get_or_none 不需要 .first()
    users = await User.get_or_none(phone=email)
    if users is None:
        return {"code":400,"error": "还没有此用户，请注册用户"}

    if users.status == 0:
        return {"code":400,"error": "账号已封禁"}
    
    # 修复：通过用户关联查密码，不要单独按密码查！
    userauth = await UserAuth.get_or_none(user_id=users.id)
    if userauth is None or userauth.credential != password:
        return {"code":400,"error": "用户密码或邮箱错误"}

    token = await register_token(email,password)
    return {"code":200,"token":token}







from fastapi import Request

# 获取客户端IP工具
def get_client_ip(request: Request):
    return request.client.host

# 发送验证码接口
@app.get("/send_email_code")
async def api_send_code(request: Request, email: str, scene: str):
    ip = get_client_ip(request)
    code = await send_email_code(email, scene, ip)
    if code:
        return {"code":200,"msg":"发送成功"}
    return {"code":500,"msg":"发送失败"}

# 校验验证码接口
@app.post("/verify_email_code")
async def api_verify(email: str, code: str,scene: str ):
    ok = await verify_code(email, code, scene)
    if ok:
        return {"code":200,"msg":"验证通过"}
    return {"code":400,"msg":"验证码错误/已过期/已使用"}


from register_login import register_user,register_auth

@app.post("/register")
async def read_user(
    email:str = Query(..., description="请输入邮箱"),
    password: str = Query(..., description="请输入注册密码"),
    scene:str = Query("register" ,description="注册场景")
    ):
    users = await User.get_or_none(phone=email)
    if users is not None:
        return {"code":400,"error": "邮箱已注册"}
    await register_user(email,scene)
    auth = await UserAuth.get_or_none(identifier=email)
    if auth is not None:

        return {"code":400,"error": "用户已绑定"}
    else:
        await register_auth(email,password)

    token = await register_token(email,password)
    return {"code":200,"msg":"注册成功","token":token}
    

# @app.get("/gettoken")
# async def read_user(phone:str,password:str):
#     token = await register_token(phone,password)
#     return {"token":token}






# ==================== 题库上传 / 导入 ====================

import os

from fastapi import File, Form, UploadFile

import import_service
from bank_parser import SUPPORTED_EXTS, get_ext, parse_file
from tortoise_models import ImportItem, ImportTask


@app.post("/upload_bank")
async def upload_bank(
    file: UploadFile = File(..., description="题库文件：xlsx / docx / pdf"),
    user_id: int = Form(..., description="上传用户ID"),
    bank_name: str = Form(None, description="题库名称，不传则取文件名"),
    subject_id: int = Form(None, description="科目ID，不传则用默认科目"),
):
    """上传题库文件并解析，结果存为待确认明细，返回预览。"""
    users = await User.get_or_none(id=user_id)
    if users is None:
        return {"code": 400, "error": "用户不存在"}

    filename = os.path.basename(file.filename or "")
    ext = get_ext(filename)
    if ext not in SUPPORTED_EXTS:
        return {
            "code": 400,
            "error": "不支持的文件类型，仅支持 .xlsx / .docx / .pdf（.xls/.doc 请先另存为新格式）",
        }

    try:
        path, filename, stored_name, ext, size = await import_service.save_upload_file(file)
        items, meta = parse_file(path)
    except ValueError as e:
        return {"code": 400, "error": str(e)}
    except Exception as e:
        return {"code": 500, "error": f"文件解析失败：{e}"}

    if not items:
        return {"code": 400, "error": "没有解析到任何题目，请检查文件是否符合题库模板"}

    task, bank = await import_service.create_import_task(
        user_id=user_id,
        bank_name=bank_name,
        subject_id=subject_id,
        filename=filename,
        stored_name=stored_name,
        ext=ext,
        file_size=size,
        items=items,
        meta=meta,
    )
    return {
        "code": 200,
        "task_id": task.id,
        "bank_id": bank.id,
        "bank_name": bank.name,
        "file_name": filename,
        "total": len(items),
        "confidence": meta.get("confidence", 0),
        "preview": items[:20],
    }


@app.get("/import_task/{task_id}/items")
async def list_import_items(
    task_id: int,
    status: str = Query(None, description="按状态过滤：pending / confirmed / rejected"),
    page: int = Query(1, description="页码，从1开始"),
    size: int = Query(50, description="每页条数，最大200"),
):
    """分页查看某个导入任务解析出来的题目，供人工确认。"""
    task = await ImportTask.get_or_none(id=task_id)
    if task is None:
        return {"code": 400, "error": "导入任务不存在"}

    query = ImportItem.filter(task_id=task_id)
    if status:
        query = query.filter(status=status)
    total = await query.count()

    page = max(page, 1)
    size = min(max(size, 1), 200)
    items = await query.order_by("seq").offset((page - 1) * size).limit(size)
    return {
        "code": 200,
        "task_id": task_id,
        "bank_id": task.bank_id,
        "task_status": task.status,
        "total": total,
        "page": page,
        "size": size,
        "items": [import_service.item_to_dict(it) for it in items],
    }


@app.post("/import_task/{task_id}/confirm")
async def confirm_import(
    task_id: int,
    item_ids: str = Query(None, description="要入库的明细ID，逗号分隔；不传则入库全部待确认项"),
):
    """人工确认后，把解析结果正式写入题目表。"""
    ids = None
    if item_ids:
        try:
            ids = [int(x) for x in item_ids.split(",") if x.strip()]
        except ValueError:
            return {"code": 400, "error": "item_ids 格式错误，应为逗号分隔的数字"}

    try:
        created = await import_service.confirm_import(task_id, ids)
    except ValueError as e:
        return {"code": 400, "error": str(e)}
    return {"code": 200, "msg": "入库成功", "created": created}


@app.post("/import_task/{task_id}/reject")
async def reject_import(
    task_id: int,
    item_ids: str = Query(None, description="要忽略的明细ID，逗号分隔；不传则忽略全部待确认项"),
):
    """把解析错的题目忽略掉，不写入题库。"""
    task = await ImportTask.get_or_none(id=task_id)
    if task is None:
        return {"code": 400, "error": "导入任务不存在"}

    ids = None
    if item_ids:
        try:
            ids = [int(x) for x in item_ids.split(",") if x.strip()]
        except ValueError:
            return {"code": 400, "error": "item_ids 格式错误，应为逗号分隔的数字"}

    rejected = await import_service.reject_items(task_id, ids)
    return {"code": 200, "msg": "已忽略", "rejected": rejected}


if __name__ == "__main__":  # 当直接运行此脚本时（而非作为模块导入时）
    import uvicorn  # 导入uvicorn ASGI服务器
    uvicorn.run("ShuTiBao_api:app", host="0.0.0.0", port=8000, reload=True)  # 启动FastAPI应用，监听所有网络接口的8000端口
