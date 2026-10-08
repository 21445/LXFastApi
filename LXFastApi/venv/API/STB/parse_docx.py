# -*- coding: utf-8 -*-
"""Word(.docx) 题库解析：把每个段落当一行文本，交给 parse_common 的行解析器。"""

import parse_deps  # noqa: F401  确保 python-docx 可导入

import docx

from parse_common import parse_text_lines


def parse(path):
    """解析 docx，返回 (题目列表, 元信息)。"""
    document = docx.Document(path)
    lines = [p.text for p in document.paragraphs]
    items = parse_text_lines(lines)
    # Word 格式规则较多，给出略低的置信度便于人工重点核对
    return items, {"page_count": 0, "confidence": 90}