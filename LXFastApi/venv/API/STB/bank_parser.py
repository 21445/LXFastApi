# -*- coding: utf-8 -*-
"""题库文件解析入口：按后缀分派到具体解析器。

统一返回 (题目列表, 元信息)，题目结构见 parse_common.build_item 的注释。
"""

import os

from parse_docx import parse as parse_docx
from parse_excel import parse as parse_excel
from parse_pdf import parse as parse_pdf

SUPPORTED_EXTS = {"xlsx", "xlsm", "docx", "pdf"}


def get_ext(filename):
    return os.path.splitext(filename or "")[1].lower().lstrip(".")


def parse_file(path):
    ext = get_ext(path)
    if ext in ("xlsx", "xlsm"):
        return parse_excel(path)
    if ext == "docx":
        return parse_docx(path)
    if ext == "pdf":
        return parse_pdf(path)
    if ext in ("xls", "doc"):
        raise ValueError(f"暂不支持旧版 .{ext} 格式，请先另存为 .{ext}x 后再上传")
    raise ValueError(f"不支持的文件类型：.{ext}，仅支持 xlsx / docx / pdf")