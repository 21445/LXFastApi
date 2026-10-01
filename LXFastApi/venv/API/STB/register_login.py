import asyncio
from enum import verify
from venv import create
from tortoise_models import User,UserAuth,UserBadge,UserMessage,SmsCode,UserToken
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from email.mime.text import MIMEText
from email.header import Header


import random
# 自动生成昵称：用户_随机4位数字
random_num = random.randint(1000,9999)
auto_nickname = f"用户_{random_num}"

import hashlib
from datetime import datetime, timedelta

def generate_token(password: str) -> str:
    """
    通过密码哈希 + 登录时间戳 生成64位SHA256 token
    :param password_hash: 用户数据库里存储的密码哈希
    :param login_time_ms: 登录时刻毫秒时间戳
    :return: 64位token字符串
    """
    login_time_ms = int(datetime.now().timestamp())
    raw_str = f"{password}|{login_time_ms}"
    sha_obj = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
    return sha_obj



async def register_user(phone:str,scene:str = "register"):
    await User.create(
    phone=phone,
    nickname=auto_nickname, #自动生成
    register_source=scene,
    status=1,
    member_level=0,
    create_time=datetime.now(),
    update_time=datetime.now(),)
    # 下面这些不填，直接用数据库默认/NULL
    return 200




async def register_auth(phone:str,password:str ,auth_type:str = "phone" ):
    users_id = await User.get_or_none(phone=phone)   



    await UserAuth.create(
            user_id = users_id.id,
            credential=password,
            verify=1,
            create_at=datetime.now(),
            auth_type=auth_type,
            identifier=phone,
    )
    
    

async def register_token(phone:str,password:str):
    user_id = await User.get_or_none(phone=phone)
    UserTok = await UserToken.get_or_none(user_id=user_id.id)
    if user_id is None:
        return {"code":400,"msg":"用户不存在"}
    elif UserTok is not None:
        await UserToken.filter(user_id=user_id.id).delete()
        
        
    
    token = generate_token(password)
    await UserToken.create(
        user_id=user_id.id,
        token=token,
        platform="web",
        device_id="",
        app_version="1.0.0",
        expire_at=datetime.now() + timedelta(days=1),
        last_active_at=datetime.now(),
        # created_at 如果模型写了 auto_now_add=True，不用传
    )
    # tokenss = await UserToken.get_or_none(user_id=user_id.id).first()
    return token

    
    
