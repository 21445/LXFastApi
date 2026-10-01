# from fastapi import FastAPI
# import requests
# import uvicorn
# import os
# import re
# import json
# import time

# app = FastAPI()


# # ============================================================
# # LM Studio 配置
# # ============================================================

# # LM Studio 本地 API
# LM_API_URL = "http://127.0.0.1:3000/api/v1/chat"

# # 如果 LM Studio 没有开启 API Authentication：
# # 留空即可
# #
# # 如果开启了 API Key：
# # 建议设置环境变量 LM_API_KEY
# LM_API_KEY = os.getenv("sk-lm-QSFge7R2:V2p5P0i1igrsZsrLj0Lt", "sk-lm-QSFge7R2:V2p5P0i1igrsZsrLj0Lt")

# # ============================================================
# # 模型名称
# # ============================================================

# # !!! 改成 LM Studio Developer 页面显示的真实模型 ID !!!
# MODEL = "qwen/qwen3.6-35b/qwen3.6-35b-a3b-claude-4.7-opus-reasoning-distilled-apex-mtp-i-compact.gguf"


# # ============================================================
# # real-browser-mcp
# # ============================================================

# # 这里非常重要：
# #
# # real-browser-mcp 现在已经由 LM Studio 管理。
# #
# # Python 不再：
# #   1. 启动 npx
# #   2. 启动 real-browser-mcp
# #   3. 创建 ClientSession
# #   4. 获取 MCP tools
# #   5. 自己执行 MCP tool
# #
# # 全部交给 LM Studio。
# #
# # 你的 MCP 在 LM Studio 中的插件 ID：
# MCP_PLUGIN = "mcp/ofershap-real-browser-mcp"


# # ============================================================
# # MCP 工具限制
# # ============================================================

# # 如果你不知道 real-browser-mcp 的具体工具名称，
# # 可以先设为 None，表示允许全部工具。
# #
# # 例如以后知道工具名称以后，可以改成：
# #
# # MCP_ALLOWED_TOOLS = [
# #     "browser_navigate",
# #     "browser_snapshot",
# #     "browser_click",
# #     "browser_type",
# # ]
# #
# MCP_ALLOWED_TOOLS = None


# # ============================================================
# # 请求参数
# # ============================================================

# REQUEST_TIMEOUT = 180

# MAX_RETRY = 2


# # ============================================================
# # LM Studio 请求头
# # ============================================================

# def get_headers():

#     headers = {
#         "Content-Type": "application/json"
#     }

#     if LM_API_KEY:
#         headers["Authorization"] = f"Bearer {LM_API_KEY}"

#     return headers


# # ============================================================
# # 获取 LM Studio 模型
# # ============================================================

# def get_models():

#     url = "http://127.0.0.1:3000/api/v1/models"

#     response = requests.get(
#         url,
#         headers=get_headers(),
#         timeout=15
#     )

#     response.raise_for_status()

#     return response.json()


# # ============================================================
# # 检查 LM Studio
# # ============================================================

# def check_lm_studio():

#     try:

#         result = get_models()

#         return {
#             "ok": True,
#             "data": result
#         }

#     except Exception as e:

#         return {
#             "ok": False,
#             "error": str(e)
#         }


# # ============================================================
# # 构造考试 Prompt
# # ============================================================

# def build_prompt(
#     title,
#     options,
#     question_type
# ):

#     prompt = f"""
# 你是一个专业的在线考试答题助手。

# 你必须根据题目判断最终答案。

# 题目：
# {title}

# 选项：
# {options}

# 题型：
# {question_type}

# ==============================
# 联网规则
# ==============================

# 如果题目涉及：

# - 当前时间
# - 今天
# - 最新消息
# - 实时数据
# - 当前价格
# - 股票
# - 基金
# - 天气
# - 新闻
# - 网站当前内容
# - 需要互联网验证的信息
# - 你无法确定的事实

# 必须优先使用 real-browser-mcp 浏览器工具查询互联网。

# 不要凭记忆猜测实时信息。

# 如果使用浏览器：

# 1. 打开相关网页
# 2. 获取网页内容
# 3. 阅读网页结果
# 4. 根据网页信息判断答案
# 5. 最后只返回答案

# ==============================
# 考试答案格式
# ==============================

# 单选题：

# 只返回一个字母：

# A

# 或者：

# B

# 或者：

# C

# 或者：

# D


# 多选题：

# 使用 # 分隔：

# A#C#D


# 判断题：

# 只能返回：

# 正确

# 或者：

# 错误


# 填空题：

# 直接返回答案。

# ==============================
# 重要规则
# ==============================

# 1. 最终只输出答案。
# 2. 不要解释。
# 3. 不要输出分析过程。
# 4. 不要输出 Markdown。
# 5. 不要输出“答案是”。
# 6. 不要输出“答案：”。
# 7. 不要输出其他内容。
# """

#     return prompt.strip()


# # ============================================================
# # 调用 LM Studio
# # ============================================================

# def call_lm_studio(
#     prompt
# ):

#     payload = {

#         "model": MODEL,

#         "input": prompt,

#         "system_prompt": (
#             "你是一个专业考试答题助手。"
#             "遇到实时信息或不确定的信息时，"
#             "必须使用浏览器 MCP 查询互联网。"
#             "最终只能输出答案。"
#         ),

#         # ====================================================
#         # 关键：
#         # 让 LM Studio 调用已经安装的 real-browser-mcp
#         # ====================================================

#         "integrations": [
#             {
#                 "type": "plugin",
#                 "id": MCP_PLUGIN
#             }
#         ],

#         # MCP 会增加很多工具描述，
#         # 所以给模型更大的上下文
#         "context_length": 16000,

#         "temperature": 0,

#         # 保存 response 状态
#         "store": True
#     }


#     print("")
#     print("================================")
#     print("请求 LM Studio")
#     print("================================")

#     print("API:", LM_API_URL)
#     print("MODEL:", MODEL)
#     print("MCP:", MCP_PLUGIN)
#     print("")

#     response = requests.post(

#         LM_API_URL,

#         headers=get_headers(),

#         json=payload,

#         timeout=REQUEST_TIMEOUT
#     )


#     print("LM Studio HTTP:", response.status_code)


#     if response.status_code != 200:

#         print("================================")
#         print("LM Studio 请求失败")
#         print(response.text)
#         print("================================")

#         raise Exception(
#             f"LM Studio HTTP {response.status_code}: "
#             f"{response.text}"
#         )


#     result = response.json()


#     print("================================")
#     print("LM Studio 返回")
#     print("================================")

#     print(
#         json.dumps(
#             result,
#             ensure_ascii=False,
#             indent=2
#         )[:10000]
#     )

#     print("================================")


#     return result


# # ============================================================
# # 从 LM Studio 新 API 响应中提取最终文本
# # ============================================================

# def extract_answer(result):

#     # ========================================================
#     # 方式 1：
#     # LM Studio /api/v1/chat 通常会提供 output
#     # ========================================================

#     output = result.get("output")


#     if isinstance(output, str):

#         return output.strip()


#     # ========================================================
#     # 方式 2：
#     # output 是数组
#     # ========================================================

#     if isinstance(output, list):

#         texts = []

#         for item in output:

#             if not isinstance(item, dict):
#                 continue

#             # text
#             if isinstance(
#                 item.get("text"),
#                 str
#             ):

#                 texts.append(
#                     item["text"]
#                 )

#             # content
#             content = item.get("content")

#             if isinstance(content, str):

#                 texts.append(content)

#             elif isinstance(content, list):

#                 for c in content:

#                     if isinstance(c, dict):

#                         text = c.get("text")

#                         if isinstance(
#                             text,
#                             str
#                         ):

#                             texts.append(text)


#         if texts:

#             return "\n".join(texts).strip()


#     # ========================================================
#     # 方式 3：
#     # 某些兼容返回
#     # ========================================================

#     choices = result.get("choices")


#     if choices:

#         try:

#             message = choices[0]["message"]

#             content = message.get(
#                 "content",
#                 ""
#             )

#             if isinstance(
#                 content,
#                 str
#             ):

#                 return content.strip()

#         except Exception:

#             pass


#     return ""


# # ============================================================
# # 清理最终答案
# # ============================================================

# def clean_answer(
#     answer,
#     question_type
# ):

#     if not answer:

#         return ""


#     answer = answer.strip()


#     # ========================================================
#     # 去 Markdown
#     # ========================================================

#     answer = answer.replace(
#         "**",
#         ""
#     )

#     answer = answer.replace(
#         "`",
#         ""
#     )


#     # ========================================================
#     # 去掉常见前缀
#     # ========================================================

#     answer = re.sub(

#         r"^(答案是|答案为|答案：|答案:)\s*",

#         "",

#         answer,

#         flags=re.IGNORECASE
#     )


#     answer = answer.strip()


#     # ========================================================
#     # 判断题
#     # ========================================================

#     if (
#         "判断" in question_type
#         or question_type.lower()
#         in ["judge", "true_false"]
#     ):

#         if "正确" in answer:

#             return "正确"


#         if "错误" in answer:

#             return "错误"


#         lower = answer.lower()

#         if lower in [
#             "true",
#             "yes",
#             "t",
#             "y"
#         ]:

#             return "正确"


#         if lower in [
#             "false",
#             "no",
#             "f",
#             "n"
#         ]:

#             return "错误"


#     # ========================================================
#     # 多选题
#     # ========================================================

#     if (
#         "多选" in question_type
#         or question_type.lower()
#         in [
#             "multiple",
#             "multi"
#         ]
#     ):

#         letters = re.findall(

#             r"\b([A-F])\b",

#             answer.upper()
#         )


#         if letters:

#             result = []

#             for letter in letters:

#                 if letter not in result:

#                     result.append(letter)


#             return "#".join(result)


#     # ========================================================
#     # 单选题
#     # ========================================================

#     letters = re.findall(

#         r"\b([A-F])\b",

#         answer.upper()
#     )


#     if letters:

#         return letters[0]


#     # ========================================================
#     # 如果模型输出类似：
#     #
#     # B。
#     # B
#     #  B
#     # ========================================================

#     match = re.match(

#         r"^\s*([A-F])\s*[。．\.\)]?\s*$",

#         answer.upper()
#     )


#     if match:

#         return match.group(1)


#     return answer


# # ============================================================
# # OCS API
# # ============================================================

# @app.post("/query")
# async def query(
#     data: dict
# ):

#     title = data.get(
#         "title",
#         ""
#     )

#     options = data.get(
#         "options",
#         ""
#     )

#     question_type = data.get(
#         "type",
#         "unknown"
#     )


#     print("")
#     print("")
#     print("================================")
#     print("收到 OCS 题目")
#     print("================================")

#     print("题目:", title)
#     print("选项:", options)
#     print("题型:", question_type)

#     print("================================")


#     try:

#         # ====================================================
#         # 检查 LM Studio
#         # ====================================================

#         status = check_lm_studio()


#         if not status["ok"]:

#             raise Exception(
#                 "LM Studio API 无法连接："
#                 + status["error"]
#             )


#         # ====================================================
#         # 构造 Prompt
#         # ====================================================

#         prompt = build_prompt(

#             title,

#             options,

#             question_type
#         )


#         # ====================================================
#         # 请求 LM Studio
#         # ====================================================

#         result = call_lm_studio(
#             prompt
#         )


#         # ====================================================
#         # 提取答案
#         # ====================================================

#         raw_answer = extract_answer(
#             result
#         )


#         print("================================")
#         print("AI 原始答案:")
#         print(raw_answer)
#         print("================================")


#         # ====================================================
#         # 清理答案
#         # ====================================================

#         answer = clean_answer(

#             raw_answer,

#             question_type
#         )


#         print("================================")
#         print("最终答案:", answer)
#         print("================================")


#         return {

#             "code": 1,

#             "data": {

#                 "question": title,

#                 "answer": answer,

#                 "raw_answer": raw_answer,

#                 "ai": True,

#                 "browser": True

#             },

#             "message": "success"
#         }


#     except requests.exceptions.Timeout:

#         print("================================")
#         print("LM Studio 请求超时")
#         print("================================")


#         return {

#             "code": 0,

#             "data": {

#                 "question": title,

#                 "answer": "AI请求超时"

#             },

#             "message": "LM Studio timeout"
#         }


#     except Exception as e:

#         print("================================")
#         print("程序异常")
#         print(type(e).__name__)
#         print(str(e))
#         print("================================")


#         return {

#             "code": 0,

#             "data": {

#                 "question": title,

#                 "answer": "AI API请求异常"

#             },

#             "message": str(e)
#         }


# # ============================================================
# # 健康检查
# # ============================================================

# @app.get("/")

# def root():

#     return {

#         "status": "ok",

#         "service": "OCS AI Answer API",

#         "lm_studio": LM_API_URL,

#         "model": MODEL,

#         "mcp": MCP_PLUGIN

#     }


# # ============================================================
# # LM Studio 状态
# # ============================================================

# @app.get("/health")

# def health():

#     status = check_lm_studio()

#     return {

#         "ok": status["ok"],

#         "lm_studio": status["ok"],

#         "mcp": MCP_PLUGIN

#     }


# # ============================================================
# # 启动
# # ============================================================

# if __name__ == "__main__":

#     print("")
#     print("================================")
#     print("OCS AI API 启动")
#     print("================================")

#     print("地址:")
#     print("http://127.0.0.1:8000")

#     print("LM Studio:")
#     print(LM_API_URL)

#     print("模型:")
#     print(MODEL)

#     print("MCP:")
#     print(MCP_PLUGIN)

#     print("================================")


#     uvicorn.run(

#         app,

#         host="0.0.0.0",

#         port=8000,

#         reload=False
#     )

from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

# ==============================
# DeepSeek API 配置
# ==============================

API_KEY = "sk-lm-5twiMOBc:03UFSnugU4pzJXh13DIA"
API_URL = "http://127.0.0.1:3000/v1/chat/completions"

# 例如：
# deepseek-chat
# deepseek-reasoner
MODEL = "qwen/qwen3.6-35b/qwen3.6-35b-a3b-claude-4.7-opus-reasoning-distilled-apex-mtp-i-compact.gguf"


# ==============================
# OCS 题目接口
# ==============================

@app.post("/query")
def query(data: dict):

    title = data.get("title", "")
    options = data.get("options", "")
    question_type = data.get("type", "unknown")

    prompt = f"""
你是一个专业的在线考试答题助手。

请根据题目和选项判断正确答案。

题目：
{title}

选项：
{options}

题型：
{question_type}

严格按照以下格式返回：

单选题：
只返回一个选项字母，例如：
B

多选题：
返回所有正确选项，并使用 # 分隔，例如：
A#C#D

判断题：
只返回：
正确
或者：
错误

填空题：
直接返回答案。

重要：
1. 不要解释。
2. 不要输出“答案是”。
3. 不要输出 Markdown。
4. 不要输出其他任何内容。
"""


    try:

        # ==============================
        # 请求 DeepSeek
        # ==============================

        r = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个只输出最终答案的考试答题助手。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0
            },
            timeout=60
        )


        # ==============================
        # HTTP 状态检查
        # ==============================

        if r.status_code != 200:

            print("================================")
            print("DeepSeek API 请求失败")
            print("HTTP状态码:", r.status_code)
            print("返回内容:", r.text)
            print("================================")

            return {
                "code": 0,
                "data": {
                    "question": title,
                    "answer": "AI API请求失败"
                },
                "message": f"HTTP {r.status_code}: {r.text}"
            }


        # ==============================
        # JSON解析
        # ==============================

        result = r.json()

        print("================================")
        print("DeepSeek API 返回：")
        print(result)
        print("================================")


        # ==============================
        # 检查 choices
        # ==============================

        if "choices" not in result:

            return {
                "code": 0,
                "data": {
                    "question": title,
                    "answer": "AI返回格式异常"
                },
                "message": str(result)
            }


        # ==============================
        # 获取AI答案
        # ==============================

        answer = result["choices"][0]["message"]["content"].strip()


        # ==============================
        # 清理AI可能输出的多余内容
        # ==============================

        answer = answer.replace("答案：", "")
        answer = answer.replace("答案是：", "")
        answer = answer.replace("答案是", "")
        answer = answer.strip()


        # ==============================
        # 返回给 OCS
        # ==============================

        return {
            "code": 1,
            "data": {
                "question": title,
                "answer": answer,
                "ai": True
            },
            "message": "success"
        }


    except requests.exceptions.Timeout:

        return {
            "code": 0,
            "data": {
                "question": title,
                "answer": "AI请求超时"
            },
            "message": "DeepSeek API timeout"
        }


    except Exception as e:

        print("================================")
        print("程序异常：")
        print(e)
        print("================================")

        return {
            "code": 0,
            "data": {
                "question": title,
                "answer": "AI API请求异常"
            },
            "message": str(e)
        }


# ==============================
# 直接运行 osc.py 时启动
# ==============================

if __name__ == "__main__":

    uvicorn.run(
        "osc1:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )