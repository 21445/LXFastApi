from fastapi import FastAPI

app = FastAPI()

from typing import Dict

# Tortoise-ORM 配置
TORTOISE_ORM: Dict = {
    "connections": {
        # 开发环境使用 SQLite（基于文件，无需服务器）
        #"default": "sqlite://db.sqlite3",
        # 生产环境示例：PostgreSQL
        # "default": "postgres://user:password@localhost:5432/dbname",
        # 生产环境示例：MySQL
        "default": "mysql://root:root@127.0.0.1:3307/fastapi_db",
    },
    "apps": {
        "models": {
            "models": ["model19", "aerich.models"],  # 模型模块和 Aerich 迁移模型
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

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True,)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("1:app", host="0.0.0.0", port=8000)
