# -*- coding: utf-8 -*-
"""题库解析的公共逻辑：题型归一化、答案归一化、纯文本行解析。

parse_excel / parse_docx / parse_pdf 共用本模块，最终都产出统一的中间结构：

    {
        "q_type":    "单选题",                          # 单选题/多选题/判断题/填空题/简答题/名词解释
        "stem":      "刷刷题的网址是",                   # 题干
        "options":   [{"label": "A", "content": "..."}], # 无选项时为 None
        "answer":    "A",                               # 判断题统一为 正确/错误；填空多空用 | 分隔
        "analysis":  "解析内容",                         # 可为 None
        "chapter":   "第一章/第一节",                    # 可为 None
        "score":     2,                                 # 可为 None
        "knowledge": None,
        "page_no":   None,
    }
"""

import re

# ============================ 常量 ============================

OPTION_LETTERS = "ABCDEFGHIJ"

_TRUE_WORDS = {"正确", "对", "是", "√", "✓", "t", "true", "y", "yes", "正确的"}
_FALSE_WORDS = {"错误", "错", "否", "不对", "×", "✗", "x", "f", "false", "n", "no"}

# 选项行：A.内容 / A、内容 / A)内容 / A：内容
OPTION_LINE_RE = re.compile(r'^([A-Ja-j])\s*[.、．)）:：]\s*(.*)$')
# 答案行：答案：xxx / 答案:xxx / 答案 xxx
ANSWER_LINE_RE = re.compile(r'^答案\s*[:：]?\s*(.*)$')
# 解析行：解析：xxx / 解析:xxx
ANALYSIS_LINE_RE = re.compile(r'^解析\s*[:：]?\s*(.*)$')
# 章节标题：第一章 / 第1节
CHAPTER_RE = re.compile(r'^第\s*[一二三四五六七八九十百零\d]+\s*[章节]')
# 题号前缀：1. / 2、 / 3)；分隔符后紧跟数字的不算，避免把 "1.5米" 误当题号
QUESTION_NO_RE = re.compile(r'^\s*(?:第\s*)?\d{1,3}\s*[.、．)）:：]\s*([^\d\s].*)$')
# 共用备选答案组，如 "（1-3题共用备选答案，常用于医护题型)"
SHARED_OPTION_RE = re.compile(r'共用\s*备选答案|备选答案\s*共用')
# 名词解释：名词:释义
NOUN_RE = re.compile(r'^(.{1,30}?)\s*[:：]\s*(.+)$')
# 普通分隔线
_SEPARATOR_CHARS = set("=-_—~ \t")

# 题型说明行 → 题型（"选择题格式" 这类不限定单/多选，映射为 None 交给推断）
_MARKER_TYPES = {
    "判断题格式": "判断题",
    "填空题格式": "填空题",
    "简答题格式": "简答题",
    "名词解释格式": "名词解释",
}


# ============================ 归一化 ============================

def normalize_q_type(t):
    """把各种写法的题型名归一化为标准名，识别不出返回 None。"""
    if not t:
        return None
    t = str(t).strip()
    if not t:
        return None
    if "多选" in t or "多项" in t:
        return "多选题"
    if "单选" in t or "单项" in t:
        return "单选题"
    if "判断" in t:
        return "判断题"
    if "填空" in t:
        return "填空题"
    if "名词解释" in t:
        return "名词解释"
    if any(k in t for k in ("简答", "问答", "论述", "计算", "案例")):
        return "简答题"
    if t == "选择题":
        return "单选题"
    return t


def normalize_judge_answer(a):
    """判断题答案归一化，返回 正确/错误，识别不出返回 None。"""
    if a is None:
        return None
    s = str(a).strip()
    if not s:
        return None
    if s in _TRUE_WORDS or s.lower() in _TRUE_WORDS:
        return "正确"
    if s in _FALSE_WORDS or s.lower() in _FALSE_WORDS:
        return "错误"
    return None


def strip_prefix(text, regex):
    """按正则取第一个分组作为内容，匹配不到则返回原文。"""
    m = regex.match(text or "")
    return m.group(1).strip() if m else (text or "").strip()


def extract_choice_letters(answer):
    """从答案里抽出选项字母并去重排序，如 "A,B" -> "AB"。"""
    return "".join(sorted(set(l.upper() for l in re.findall(r'[A-Ja-j]', answer or ""))))


def extract_inline_answer(stem):
    """从题干末尾括号里提取内嵌答案。

    返回 (新题干, 答案, 是否是判断题答案)。
    只有括号内容"看起来像答案"时才提取，否则原样返回（避免把填空题括号误当答案）。
    """
    if not stem:
        return stem, None, False
    m = re.search(r'[（(]\s*([^（）()]{0,60}?)\s*[)）]\s*$', stem)
    if not m:
        return stem, None, False
    inner = m.group(1).strip()
    if not inner:
        return stem, None, False
    if re.fullmatch(r'[A-Ja-j]{1,10}', inner):
        return stem[:m.start()].strip(), inner.upper(), False
    j = normalize_judge_answer(inner)
    if j:
        return stem[:m.start()].strip(), j, True
    return stem, None, False


def infer_q_type(stem, options, answer):
    """没有明确题型时按结构推断。"""
    if options:
        letters = set(re.findall(r'[A-Ja-j]', answer or ""))
        return "多选题" if len(letters) > 1 else "单选题"
    if normalize_judge_answer(answer):
        return "判断题"
    if re.search(r'(_{2,}|（\s*）|\(\s*\))', stem or ""):
        return "填空题"
    return "简答题"


# ============================ 单题归一化 ============================

def build_item(raw):
    """把原始 dict 归一化成统一中间结构，题干为空则返回 None。"""
    stem = (raw.get("stem") or "").strip()
    if not stem:
        return None

    # 选项去重、按字母排序
    options = []
    seen = set()
    for o in raw.get("options") or []:
        label = (o.get("label") or "").strip().upper()
        if not label or label in seen:
            continue
        seen.add(label)
        options.append({"label": label, "content": (o.get("content") or "").strip()})
    options.sort(key=lambda o: o["label"])

    q_type = normalize_q_type(raw.get("q_type"))

    new_stem, inline_answer, inline_is_judge = extract_inline_answer(stem)
    answer = (raw.get("answer") or "").strip()
    if inline_answer:
        stem = new_stem
        answer = answer or inline_answer
    if inline_is_judge and not q_type:
        q_type = "判断题"

    if not q_type:
        q_type = infer_q_type(stem, options, answer)

    if q_type == "判断题":
        answer = normalize_judge_answer(answer) or answer or "正确"
        options = [{"label": "A", "content": "正确"}, {"label": "B", "content": "错误"}]
    elif q_type in ("单选题", "多选题") and options:
        letters = extract_choice_letters(answer)
        if letters:
            answer = letters

    return {
        "q_type": q_type,
        "stem": stem,
        "options": options or None,
        "answer": answer or None,
        "analysis": (raw.get("analysis") or "").strip() or None,
        "chapter": (raw.get("chapter") or "").strip() or None,
        "score": raw.get("score"),
        "knowledge": (raw.get("knowledge") or "").strip() or None,
        "page_no": raw.get("page_no"),
    }


# ============================ 纯文本行解析（docx / pdf 共用） ============================

def _is_separator(s):
    return bool(s) and set(s) <= _SEPARATOR_CHARS


def _is_chapter_header(s):
    """像章节标题才认，题干里带问号的直接排除。"""
    if not s or len(s) > 40 or "？" in s or "?" in s:
        return False
    if re.match(r'^[一二三四五六七八九十]+\s*[、.．]', s):
        return True
    return bool(CHAPTER_RE.match(s))


def _clean_chapter(s):
    s = re.sub(r'^[一二三四五六七八九十]+\s*[、.．]\s*', '', s).strip()
    s = re.sub(r'[（(][^（）()]*[)）]\s*$', '', s).strip()
    return s or None


def _format_marker(s):
    """识别"XX格式"这类排版说明行，返回 (是否标记行, 题型或None)。"""
    if not s or len(s) > 40:
        return False, None
    if "共用题干" in s:
        return True, None
    if s.endswith("格式"):
        if "选择" in s:
            return True, None
        return True, normalize_q_type(s) or _MARKER_TYPES.get(s)
    return False, None


def parse_text_lines(lines):
    """把逐行文本解析成题目列表（Word / PDF 共用）。"""
    items = []
    section_raw = []      # 当前章节段落内的原始题目，供 [试卷答案] 按序回填
    shared_options = []   # 共用备选答案池，后续题目默认带上这套选项
    shared_mode = False   # 是否正在收集共用备选答案
    cur_raw = None
    chapter = None
    type_hint = None
    answer_mode = False   # 是否处于 [试卷答案] 区块
    answer_cursor = 0
    last_raw = None

    def new_raw(stem):
        return {
            "stem": stem,
            "options": [dict(o) for o in shared_options],
            "answer": "",
            "analysis": None,
            "chapter": chapter,
            "q_type": type_hint,
            "score": None,
            "knowledge": None,
            "page_no": None,
        }

    def flush_cur():
        nonlocal cur_raw
        if cur_raw is not None:
            if (cur_raw.get("stem") or "").strip():
                section_raw.append(cur_raw)
            cur_raw = None

    def finalize_section():
        nonlocal section_raw, answer_cursor
        for raw in section_raw:
            item = build_item(raw)
            if item:
                items.append(item)
        section_raw = []
        answer_cursor = 0

    for line in lines:
        s = (line or "").strip()
        if not s or _is_separator(s):
            continue

        # ---- 试卷答案区块开始 ----
        if s in ("[试卷答案]", "【试卷答案】", "试卷答案"):
            flush_cur()
            answer_mode = True
            answer_cursor = 0
            last_raw = None
            continue

        # ---- 章节标题 ----
        if _is_chapter_header(s):
            flush_cur()
            finalize_section()
            chapter = _clean_chapter(s)
            type_hint = None
            shared_options = []
            shared_mode = False
            answer_mode = False
            continue

        # ---- 题型说明行 ----
        is_marker, marker_type = _format_marker(s)
        if is_marker:
            flush_cur()
            type_hint = marker_type
            shared_options = []
            shared_mode = False
            answer_mode = False
            continue

        # ---- 共用备选答案组：下面几行选项供后续多题共用 ----
        if SHARED_OPTION_RE.search(s):
            flush_cur()
            shared_options = []
            shared_mode = True
            type_hint = "单选题"
            answer_mode = False
            continue

        # ---- 试卷答案区块内容 ----
        if answer_mode:
            if s.startswith("解析"):
                if last_raw is not None:
                    last_raw["analysis"] = strip_prefix(s, ANALYSIS_LINE_RE)
                continue
            m = re.match(r'^(\d+)\s*[.、．)）:：]\s*(.+)$', s)
            if m:
                idx = int(m.group(1))
                target = section_raw[idx - 1] if 1 <= idx <= len(section_raw) else None
                value = m.group(2).strip()
            else:
                target = section_raw[answer_cursor] if answer_cursor < len(section_raw) else None
                value = s
                answer_cursor += 1
            if target is not None:
                target["answer"] = value
                last_raw = target
            continue

        # ---- 选项 ----
        m = OPTION_LINE_RE.match(s)
        if m:
            option = {"label": m.group(1).upper(), "content": m.group(2).strip()}
            if cur_raw is not None:
                cur_raw["options"].append(option)
            elif shared_mode:
                shared_options.append(option)
            continue

        # ---- 答案 / 解析 ----
        if s.startswith("答案"):
            if cur_raw is not None:
                cur_raw["answer"] = strip_prefix(s, ANSWER_LINE_RE)
            continue
        if s.startswith("解析"):
            if cur_raw is not None:
                cur_raw["analysis"] = strip_prefix(s, ANALYSIS_LINE_RE)
            continue

        # ---- 名词解释：名词:释义 单行成题 ----
        if type_hint == "名词解释":
            noun = NOUN_RE.match(s)
            if noun:
                flush_cur()
                cur_raw = new_raw(noun.group(1).strip())
                cur_raw["q_type"] = "名词解释"
                cur_raw["answer"] = noun.group(2).strip()
                flush_cur()
                continue

        # ---- 其余行视为新题目的题干（去掉行首题号）----
        flush_cur()
        shared_mode = False
        no_match = QUESTION_NO_RE.match(s)
        cur_raw = new_raw(no_match.group(1).strip() if no_match else s)

    flush_cur()
    finalize_section()
    return items