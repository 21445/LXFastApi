# -*- coding: utf-8 -*-
"""PDF 题库解析。

PDF 的文字提取顺序经常被排版打乱（题干、选项、答案可能交错），
这里按页提取文本后再走和 Word 一样的行解析，属于尽力而为：
置信度给低分，提醒使用者务必人工核对。
"""

import parse_deps  # noqa: F401  确保 pdfplumber 可导入

import pdfplumber

from parse_common import parse_text_lines


def parse(path):
    """解析 pdf，返回 (题目列表, 元信息)。"""
    lines = []
    page_count = 0
    with pdfplumber.open(path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines.extend(text.splitlines())

    items = parse_text_lines(lines)
    return items, {"page_count": page_count, "confidence": 50}