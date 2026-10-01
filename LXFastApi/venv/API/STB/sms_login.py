from ast import main
import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
from tkinter import image_names
from tortoise_models import SmsCode
import asyncio


MAIL_FROM = "2070881724@qq.com"
MAIL_AUTH_CODE = "jjstejsfzjnnbbhf"
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 465





async def send_email_code(recv_account: str, scene: str, client_ip: str):
    """
    recv_account: 用户邮箱（填入phone字段）
    scene: 场景 register / login
    client_ip: 请求端IP，存入send_ip
    return: 成功返回code，失败返回None
    """
    # 生成6位验证码
    code = f"{random.randint(100000, 999999)}"
    now = datetime.now()
    print(now)
    expire_at = now + timedelta(minutes=5)


    title = "【验证码】你的邮箱验证码"
    content = f"您好！\n您的验证码是：{code}\n有效期5分钟，请尽快使用。\n请勿泄露给他人。"

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = Header(title, "utf-8").encode()
    msg["From"] = MAIL_FROM
    msg["To"] = recv_account

    try:
        # 同步smtp放到线程，不阻塞FastAPI
        def send_mail():
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(MAIL_FROM, MAIL_AUTH_CODE)
                server.send_message(msg)
        await asyncio.to_thread(send_mail)

        # 【发送新码前】删除该账号同场景下，未过期旧验证码
        await SmsCode.filter(
            phone=recv_account,
            scene=scene,
            expire_at__gt=now,
            used_at__isnull=True
        ).delete()

        # 新增记录到数据库
        await SmsCode.create(
            phone=recv_account,
            code=code,
            scene=scene,
            send_ip=client_ip,
            expire_at=expire_at,
            used_at=None,
            created_at=now
        )
        print(f"✅ 验证码发送成功 -> {recv_account}, code={code}, scene={scene}")
        return code
    except Exception as e:
        print(f"❌ 发送失败: {str(e)}")
        return None

async def verify_code(recv_account: str, scene: str, input_code: str) -> bool:
    """
    校验验证码
    return True=验证通过；False=失败
    """
    now = datetime.now()
    # 查询：账号匹配、场景匹配、未过期、未使用
    record = await SmsCode.filter(
        phone=recv_account,
        scene=scene,
        code=input_code,
        expire_at__gt=now,
        used_at__isnull=True
    ).first()

    if record:
        # 验证成功，写入核销时间，标记已使用，防止重复使用
        record.delete()
        return True
    return False

