# -*- coding: utf-8 -*-
"""Excel 题库解析。

表头形如：
    大题题干 | 题型(选填) | 题目/题干/小题题干 | 选项A..选项J | 答案 | 解析 | 章节 | 知识点 | 分值

按表头名字定位列（不依赖列顺序），多个 sheet 都会解析。
"""

import parse_deps  # noqa: F401  确保 openpyxl 可导入

import openpyxl

from parse_common import OPTION_LETTERS, build_item


def _normalize_header(value):
    h = (value or "").strip()
    h = h.replace("（", "(").replace("）", ")").replace(" ", "")
    return h


def _resolve_header(value):
    """把表头单元格映射成内部字段名，识别不出返回 None。"""
    h = _normalize_header(value)
    if not h:
        return None
    if h.startswith("选项"):
        tail = h[2:].strip().upper()
        if tail and tail[0] in OPTION_LETTERS:
            return "option_" + tail[0]
        return None
    if h.startswith("题型"):
        return "q_type"
    if h == "答案":
        return "answer"
    if "解析" in h:
        return "analysis"
    if "章节" in h:
        return "chapter"
    if "知识点" in h:
        return "knowledge"
    if "分值" in h or "分数" in h:
        return "score"
    if "题干" in h:
        return "group_stem" if "大题" in h else "stem"
    return None


def _cell(row, idx):
    if idx is None or idx >= len(row):
        return None
    value = row[idx]
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _row_to_raw(row, col_map):
    stem = _cell(row, col_map.get("stem"))
    q_type = _cell(row, col_map.get("q_type"))
    if not stem and not q_type:
        return None

    options = []
    for letter in OPTION_LETTERS:
        idx = col_map.get("option_" + letter)
        if idx is None:
            continue
        content = _cell(row, idx)
        if content is None:
            continue
        options.append({"label": letter, "content": content})

    score = None
    score_text = _cell(row, col_map.get("score"))
    if score_text:
        try:
            score = float(score_text)
        except ValueError:
            score = None

    return {
        "stem": stem,
        "q_type": q_type,
        "options": options,
        "answer": _cell(row, col_map.get("answer")),
        "analysis": _cell(row, col_map.get("analysis")),
        "chapter": _cell(row, col_map.get("chapter")),
        "knowledge": _cell(row, col_map.get("knowledge")),
        "score": score,
        "page_no": None,
    }


def parse(path):
    """解析 xlsx，返回 (题目列表, 元信息)。"""
    workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
    items = []
    try:
        for sheet in workbook.worksheets:
            rows = list(sheet.iter_rows(values_only=True))
            header_index = None
            col_map = {}
            for i, row in enumerate(rows):
                mapping = {}
                for j, cell in enumerate(row):
                    key = _resolve_header(cell)
                    if key:
                        mapping[key] = j
                if "stem" in mapping:
                    header_index = i
                    col_map = mapping
                    break
            if header_index is None:
                continue
            for row in rows[header_index + 1:]:
                raw = _row_to_raw(row, col_map)
                if raw is None:
                    continue
                item = build_item(raw)
                if item:
                    items.append(item)
    finally:
        workbook.close()

    return items, {"page_count": 0, "confidence": 100}