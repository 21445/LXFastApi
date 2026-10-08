# -*- coding: utf-8 -*-
"""让解析依赖（openpyxl / python-docx / pdfplumber）可被导入。

项目当前把这些库装在了 d:\\LXFastApi\\_pylibs（沙箱不允许写入系统 site-packages）。
这里统一做一次 path 兜底：如果系统里已经正常安装，则优先用系统里的。
可通过环境变量 LX_PYLIBS 覆盖默认路径。
"""

import os
import sys

_LIBS = os.environ.get("LX_PYLIBS") or r"D:\LXFastApi\_pylibs"

if os.path.isdir(_LIBS) and _LIBS not in sys.path:
    sys.path.append(_LIBS)