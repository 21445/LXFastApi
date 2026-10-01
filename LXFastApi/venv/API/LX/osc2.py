from fastapi import FastAPI
import requests
import uvicorn
import re
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

app = FastAPI()


# ============================================================
# LM Studio 配置
# ============================================================

LM_API_URL = "http://127.0.0.1:3000/v1/chat/completions"

# 如果 LM Studio 没有开启 API Key，留空即可
LM_API_KEY = "sk-lm-5twiMOBc:03UFSnugU4pzJXh13DIA"

MODEL = "qwen/qwen3.6-35b/qwen3.6-35b-a3b-claude-4.7-opus-reasoning-distilled-apex-mtp-i-compact.gguf"


# ============================================================
# 联网搜索配置
# ============================================================

# True = 开启联网
ENABLE_WEB_SEARCH = True

# 最多使用几个搜索结果
MAX_SEARCH_RESULTS = 5

# 搜索超时时间
SEARCH_TIMEOUT = 10


# ============================================================
# 搜索引擎
# ============================================================

def web_search(query: str):

    """
    使用 DuckDuckGo HTML 搜索。

    不需要额外购买搜索 API。
    如果搜索失败，会自动返回空结果。
    """

    try:

        print("\n========================================")
        print("开始联网搜索")
        print("========================================")
        print("搜索:", query)

        url = "https://html.duckduckgo.com/html/"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        }

        response = requests.post(
            url,
            data={
                "q": query
            },
            headers=headers,
            timeout=SEARCH_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for item in soup.select(".result"):

            title_element = item.select_one(".result__title")

            link_element = item.select_one(".result__a")

            snippet_element = item.select_one(
                ".result__snippet"
            )

            if not title_element or not link_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True
            )

            link = link_element.get("href", "")

            snippet = ""

            if snippet_element:
                snippet = snippet_element.get_text(
                    " ",
                    strip=True
                )

            if not link:
                continue

            results.append({
                "title": title,
                "url": link,
                "snippet": snippet
            })

            if len(results) >= MAX_SEARCH_RESULTS:
                break


        print("搜索结果数量:", len(results))

        for i, item in enumerate(results, 1):

            print(
                f"[{i}] {item['title']}"
            )

        return results


    except Exception as e:

        print("\n========================================")
        print("联网搜索失败")
        print("========================================")
        print(e)

        return []


# ============================================================
# 判断是否需要联网
# ============================================================

def need_web_search(title, question_type):

    """
    自动判断是否需要联网。

    目前采用关键词 + 题目类型判断。
    """

    keywords = [
        "现在",
        "当前",
        "今天",
        "今日",
        "目前",
        "最新",
        "最近",
        "实时",
        "新闻",
        "消息",
        "时间",
        "几点",
        "多少点",
        "天气",
        "汇率",
        "股价",
        "价格",
        "排名",
        "冠军",
        "赛程",
        "比分",
        "比赛",
        "世界杯",
        "2026",
        "2025",
        "2024",
        "刚刚",
        "近期",
        "最新消息"
    ]

    for keyword in keywords:

        if keyword in title:
            return True

    # 判断题比较容易涉及当前事实
    if question_type == "judgement":

        return True

    return False


# ============================================================
# 构造联网搜索上下文
# ============================================================

def build_web_context(results):

    if not results:

        return "没有获取到联网搜索结果。"


    text = "\n\n========== 联网搜索结果 ==========\n"

    for i, item in enumerate(results, 1):

        text += f"""
【搜索结果 {i}】

标题：
{item['title']}

网址：
{item['url']}

摘要：
{item['snippet']}

"""


    text += "========== 联网搜索结果结束 ==========\n"

    return text


# ============================================================
# 调用 LM Studio
# ============================================================

def ask_qwen(
    title,
    options,
    question_type,
    web_context=""
):

    # 服务器本地实时时间（用于“现在几点/今天是几号”等实时问题，
    # 联网搜索的摘要里没有具体时间，必须由代码直接注入）
    now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

    prompt = f"""
你是一个专业的在线考试答题助手。

请根据题目、选项以及必要的联网信息判断正确答案。

====================
当前实时时间
====================

（服务器本地时间，北京时间）

{now_str}

====================
题目
====================

{title}


====================
选项
====================

{options}


====================
题型
====================

{question_type}


====================
联网搜索信息
====================

{web_context}


====================
答案格式
====================

单选题：

只返回一个选项字母。

例如：

B


多选题：

返回所有正确选项，并使用 # 分隔。

例如：

A#C#D


判断题：

只返回：

正确

或者：

错误


填空题：

直接返回答案。


====================
重要要求
====================

1. 只输出最终答案。
2. 不要解释。
3. 不要输出“答案是”。
4. 不要输出 Markdown。
5. 不要输出分析过程。
6. 多选题必须使用 # 分隔。
7. 必须仔细阅读并分析上面的联网搜索结果，结合其中的信息作答。
8. 如果联网信息与自己的知识冲突，优先考虑可靠的联网信息。
9. 不要把搜索结果中的网址作为答案。
10. 如果题目询问当前时间或日期，必须以“当前实时时间”一栏为准，不要使用自己训练数据中的时间。
"""


    headers = {
        "Content-Type": "application/json"
    }

    if LM_API_KEY:

        headers["Authorization"] = (
            f"Bearer {LM_API_KEY}"
        )


    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "system",
                "content": (
                    "你是一个专业的考试答题助手。"
                    "必须只输出最终答案。"
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        "temperature": 0,

        # 推理模型会先输出思考过程，100 个 token 可能全被思考耗尽，
        # 导致最终答案为空（联网数据会让思考更长）。调大以留足输出空间。
        "max_tokens": 2048
    }


    response = requests.post(
        LM_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )


    if response.status_code != 200:

        raise Exception(
            f"LM Studio HTTP {response.status_code}: "
            f"{response.text}"
        )


    result = response.json()


    if "choices" not in result:

        raise Exception(
            f"LM Studio返回格式异常: {result}"
        )


    if not result["choices"]:

        raise Exception(
            "LM Studio choices为空"
        )


    message = (
        result["choices"][0]
        ["message"]
    )

    # 优先取 content；部分推理模型会把最终答案写在 reasoning_content 中，
    # 若 content 为空则回退读取 reasoning_content
    answer = (
        message.get("content")
        or message.get("reasoning_content")
        or ""
    )


    return answer.strip()


# ============================================================
# 答案清洗
# ============================================================

def clean_answer(answer, question_type):

    if not answer:

        return ""


    answer = answer.strip()


    # --------------------------------------------
    # 删除常见前缀
    # --------------------------------------------

    remove_words = [
        "答案：",
        "答案:",
        "答案是：",
        "答案是:",
        "答案是",
        "最终答案：",
        "最终答案:",
        "最终答案是：",
        "最终答案是:"
    ]

    for word in remove_words:

        answer = answer.replace(
            word,
            ""
        )


    answer = answer.strip()


    # --------------------------------------------
    # 单选题
    # --------------------------------------------

    if question_type == "single":

        match = re.search(
            r"\b([A-Z])\b",
            answer.upper()
        )

        if match:

            return match.group(1)


        # 兼容 "B." / "B、"
        match = re.search(
            r"^\s*([A-Z])[\.\、\s]",
            answer.upper()
        )

        if match:

            return match.group(1)


    # --------------------------------------------
    # 多选题
    # --------------------------------------------

    if question_type == "multiple":

        letters = re.findall(
            r"\b([A-Z])\b",
            answer.upper()
        )

        unique = []

        for letter in letters:

            if letter not in unique:

                unique.append(letter)


        if unique:

            return "#".join(unique)


    # --------------------------------------------
    # 判断题
    # --------------------------------------------

    if question_type == "judgement":

        if "正确" in answer:

            return "正确"

        if "错误" in answer:

            return "错误"

        if answer.lower() in [
            "true",
            "yes"
        ]:

            return "正确"

        if answer.lower() in [
            "false",
            "no"
        ]:

            return "错误"


    return answer.strip()


# ============================================================
# OCS API
# ============================================================

@app.post("/query")
def query(data: dict):

    title = data.get(
        "title",
        ""
    )

    options = data.get(
        "options",
        ""
    )

    question_type = data.get(
        "type",
        "unknown"
    )


    print("\n\n")
    print("========================================")
    print("收到 OCS 题目")
    print("========================================")

    print("题目:")
    print(title)

    print("\n选项:")
    print(options)

    print("\n题型:")
    print(question_type)


    try:

        # ====================================================
        # 判断是否需要联网
        # ====================================================

        use_web = False

        if ENABLE_WEB_SEARCH:

            use_web = need_web_search(
                title,
                question_type
            )


        web_context = ""


        # ====================================================
        # 联网搜索
        # ====================================================

        if use_web:

            search_query = title

            # 把选项也加入搜索
            if options:

                search_query += " " + options


            results = web_search(
                search_query
            )


            web_context = build_web_context(
                results
            )

        else:

            print("\n本题不需要联网搜索")


        # ====================================================
        # 调用 Qwen
        # ====================================================

        print("\n========================================")
        print("请求 LM Studio")
        print("========================================")

        print("API:")
        print(LM_API_URL)

        print("MODEL:")
        print(MODEL)

        print("联网:")
        print("是" if use_web else "否")


        answer = ask_qwen(
            title,
            options,
            question_type,
            web_context
        )


        print("\n========================================")
        print("Qwen原始答案")
        print("========================================")

        print(answer)


        # ====================================================
        # 清洗答案
        # ====================================================

        answer = clean_answer(
            answer,
            question_type
        )


        print("\n========================================")
        print("最终答案")
        print("========================================")

        print(answer)


        # ====================================================
        # 返回 OCS
        # ====================================================

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

        print("\nLM Studio / 搜索请求超时")


        return {

            "code": 0,

            "data": {

                "question": title,

                "answer": "AI请求超时"

            },

            "message": "request timeout"
        }


    except requests.exceptions.ConnectionError as e:

        print("\n无法连接 LM Studio 或联网搜索")

        print(e)


        return {

            "code": 0,

            "data": {

                "question": title,

                "answer": "无法连接AI服务"

            },

            "message": str(e)
        }


    except Exception as e:

        print("\n========================================")
        print("程序异常")
        print("========================================")

        print(e)


        return {

            "code": 0,

            "data": {

                "question": title,

                "answer": "AI API请求异常"

            },

            "message": str(e)
        }


# ============================================================
# 启动 FastAPI
# ============================================================

if __name__ == "__main__":

    uvicorn.run(

        "osc2:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )