#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型启动脚本 - 支持多模型切换
每个模型独立配置，根据 RTX 3080 20GB + E5-2698 v3 优化
"""

import os
import subprocess
import sys
import threading

# ==================== 配置区域 ====================
# 每个模型的独立配置参数
MODELS = {
    1: {
        "name": "① Qwen3.6-35B-A3B - IQ4_NL (推荐)",
        "path": r"E:\llamacpp\models\Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ4_NL.gguf",
        "mmproj": r"E:\llamacpp\models\mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "vision",
        # ===== 模型专用参数 =====
        "alias": "Qwen36_35B_IQ4NL",
        "ngl": 37,           # 全层GPU，~20GB 刚好塞进 20G 显存
        "threads": 16,        # E5-2698 v3 物理核心数
        "context": 102400,    # 超高上下文
        "keep": 32768,        # 活跃保留窗口
        "batch": 256,
        "ubatch": 128,
    },
    2: {
        "name": "② Qwen3.6-35B-A3B - Q4_K_P",
        "path": r"E:\llamacpp\models\Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_P.gguf",
        "mmproj": r"E:\llamacpp\models\mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "vision",
        # ===== 模型专用参数 =====
        "alias": "Qwen36_35B_Q4KP",
        "ngl": 30,           # Q4_K_P 比 IQ4_NL 大，减少GPU层数
        "threads": 16,
        "context": 65536,    # 模型较大，适当降低上下文
        "keep": 16384,
        "batch": 256,
        "ubatch": 128,
    },
    3: {
        "name": "③ Qwen3.6-35B-A3B - IQ2_M (极速)",
        "path": r"E:\llamacpp\models\Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M.gguf",
        "mmproj": r"E:\llamacpp\models\mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "vision",
        # ===== 模型专用参数 =====
        "alias": "Qwen36_35B_IQ2M",
        "ngl": 37,           # IQ2_M 很小，全层GPU无压力
        "threads": 16,
        "context": 102400,
        "keep": 32768,
        "batch": 512,        # 模型小，可以拉高batch提速
        "ubatch": 256,
    },
    4: {
        "name": "④ Qwen3.6-27B - Q4_K_P",
        "path": r"E:\llamacpp\models\Qwen3.6-27B-Uncensored-HauhauCS-Aggressive-Q4_K_P.gguf",
        "mmproj": r"E:\llamacpp\models\mmproj-Qwen3.6-27B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "vision",
        # ===== 模型专用参数 =====
        "alias": "Qwen36_27B_Q4KP",
        "ngl": 37,           # 27B 全层GPU轻松
        "threads": 16,
        "context": 102400,
        "keep": 32768,
        "batch": 256,
        "ubatch": 128,
    },
    5: {
        "name": "⑤ mmproj-35B-A3B (视觉编码器)",
        "path": r"E:\llamacpp\models\mmproj-Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "mmproj",
        # ===== 模型专用参数 =====
        "alias": "mmproj_35B",
        "ngl": 99,           # mmproj 极小，全量GPU
        "threads": 16,
        "context": 8192,
        "keep": 4096,
        "batch": 512,
        "ubatch": 512,
    },
    6: {
        "name": "⑥ mmproj-27B (视觉编码器)",
        "path": r"E:\llamacpp\models\mmproj-Qwen3.6-27B-Uncensored-HauhauCS-Aggressive-f16.gguf",
        "type": "mmproj",
        # ===== 模型专用参数 =====
        "alias": "mmproj_27B",
        "ngl": 99,
        "threads": 16,
        "context": 8192,
        "keep": 4096,
        "batch": 512,
        "ubatch": 512,
    },
}

# llama-server 可执行文件路径
LLAMA_SERVER_EXE = r".\llama-server.exe"

# 全局默认参数（模型未指定时使用）
DEFAULT_PARAMS = {
    "jinja": True,
    "no_mmap": True,
    "no_host": True,
    "reasoning": "auto",
    "context_shift": True,
    "api_key": "sk_local123456",
    "flash_attn": "auto",
    "cache_type_k": "q4_0",
    "cache_type_v": "q4_0",
    "host": "127.0.0.1",
    "port": 8080,
}
# ================================================


def check_llama_server():
    """检查 llama-server.exe 是否存在"""
    if not os.path.exists(LLAMA_SERVER_EXE):
        print(f"❌ 错误: 找不到 {LLAMA_SERVER_EXE}")
        print(f"   请确保 llama-server.exe 在当前目录")
        input("按回车键退出...")
        return False
    return True


def check_model_path(model_path):
    """检查模型文件是否存在"""
    return os.path.exists(model_path)


def build_command(model_path, model_info, load_mmproj=False):
    """构建 llama-server 启动命令（使用每模型独立参数）"""
    cmd = [LLAMA_SERVER_EXE, "-m", model_path]

    # ===== 视觉模型可选加载 mmproj =====
    if load_mmproj and model_info.get("mmproj"):
        mmproj_path = model_info["mmproj"]
        if check_model_path(mmproj_path):
            cmd.extend(["--mmproj", mmproj_path])
            print(f"👁️ 已加载视觉编码器: {mmproj_path}")
        else:
            print(f"⚠️  警告: mmproj文件不存在")
    elif load_mmproj and not model_info.get("mmproj"):
        print(f"⚠️  该模型未配置 mmproj")

    # ===== 模型专用参数 > 全局默认参数 =====
    # 优先用模型自己的参数，没有则用全局默认
    ngl = model_info.get("ngl", DEFAULT_PARAMS.get("ngl"))
    threads = model_info.get("threads", DEFAULT_PARAMS.get("threads"))
    ctx = model_info.get("context", DEFAULT_PARAMS.get("context"))
    keep = model_info.get("keep", DEFAULT_PARAMS.get("keep"))
    batch = model_info.get("batch", DEFAULT_PARAMS.get("batch"))
    ubatch = model_info.get("ubatch", DEFAULT_PARAMS.get("ubatch"))

    # --alias
    if model_info.get("alias"):
        cmd.extend(["--alias", model_info["alias"]])
    # -ngl
    if ngl:
        cmd.extend(["-ngl", str(ngl)])
    # 固定参数
    if DEFAULT_PARAMS.get("jinja"):
        cmd.append("--jinja")
    if DEFAULT_PARAMS.get("no_mmap"):
        cmd.append("--no-mmap")
    if DEFAULT_PARAMS.get("no_host"):
        cmd.append("--no-host")
    if DEFAULT_PARAMS.get("reasoning"):
        cmd.extend(["--reasoning", DEFAULT_PARAMS["reasoning"]])
    # -c
    if ctx:
        cmd.extend(["-c", str(ctx)])
    if DEFAULT_PARAMS.get("context_shift"):
        cmd.append("--context-shift")
    # --keep
    if keep:
        cmd.extend(["--keep", str(keep)])
    # --api-key
    if DEFAULT_PARAMS.get("api_key"):
        cmd.extend(["--api-key", DEFAULT_PARAMS["api_key"]])
    # -fa
    if DEFAULT_PARAMS.get("flash_attn"):
        cmd.extend(["-fa", DEFAULT_PARAMS["flash_attn"]])
    # -t
    if threads:
        cmd.extend(["-t", str(threads)])
    # -b
    if batch:
        cmd.extend(["-b", str(batch)])
    # -ub
    if ubatch:
        cmd.extend(["-ub", str(ubatch)])
    # cache types
    if DEFAULT_PARAMS.get("cache_type_k"):
        cmd.extend(["--cache-type-k", DEFAULT_PARAMS["cache_type_k"]])
    if DEFAULT_PARAMS.get("cache_type_v"):
        cmd.extend(["--cache-type-v", DEFAULT_PARAMS["cache_type_v"]])
    # host / port
    if DEFAULT_PARAMS.get("host"):
        cmd.extend(["--host", DEFAULT_PARAMS["host"]])
    if DEFAULT_PARAMS.get("port"):
        cmd.extend(["--port", str(DEFAULT_PARAMS["port"])])

    return cmd


def format_params_display(model_info):
    """生成参数字符串用于显示"""
    parts = []
    if model_info.get("alias"):
        parts.append(f"alias={model_info['alias']}")
    parts.append(f"ngl={model_info.get('ngl', 'default')}")
    parts.append(f"t={model_info.get('threads', 'default')}")
    parts.append(f"c={model_info.get('context', 'default')}")
    parts.append(f"keep={model_info.get('keep', 'default')}")
    parts.append(f"b={model_info.get('batch', 'default')}")
    parts.append(f"ub={model_info.get('ubatch', 'default')}")
    return " | ".join(parts)


def run_server(model_info, load_mmproj=False):
    """运行 llama-server"""
    alias = model_info.get("alias", "unknown")
    port = DEFAULT_PARAMS.get("port", 8080)

    print(f"\n{'='*60}")
    print(f"🚀 启动: {model_info['name']}")
    print(f"📁 模型: {model_info['path']}")
    if load_mmproj:
        print(f"👁️ 模式: 视觉模型（含图像识别）")
    else:
        print(f"💬 模式: 纯文本对话")
    print(f"⚙️  参数: {format_params_display(model_info)}")
    print(f"🌐 地址: http://127.0.0.1:{port}")
    print(f"{'='*60}\n")

    cmd = build_command(model_info["path"], model_info, load_mmproj)
    print(f"$ {' '.join(cmd)}\n")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )

        def output_logger():
            for line in process.stdout:
                print(line, end="")

        logger_thread = threading.Thread(target=output_logger, daemon=True)
        logger_thread.start()

        process.wait()

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断，正在关闭服务器...")
        process.terminate()
        process.wait()
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        return False

    return True


def print_menu():
    """打印菜单"""
    print("\n" + "=" * 60)
    print("🤖 多模型切换启动脚本")
    print(f"💻 E5-2698 v3 | RTX 3080 20GB | 24GB RAM")
    print("=" * 60)
    print("\n📋 可用模型:\n")

    for model_id, model_info in MODELS.items():
        exists = "✅" if check_model_path(model_info["path"]) else "❌"
        model_type = model_info.get("type", "text")
        type_tag = (
            "👁️视觉"
            if model_type == "vision"
            else "🎯mmproj"
            if model_type == "mmproj"
            else "💬文本"
        )
        params_str = format_params_display(model_info)
        print(f"  [{model_id}] {exists} {type_tag} {model_info['name']}")
        print(f"         ⚙️  {params_str}")

    print("\n" + "-" * 60)
    print("  输入模型编号启动 (1-6)")
    print("  输入 'q' 退出程序")
    print("=" * 60 + "\n")


def switch_model():
    """交互式切换模型"""
    while True:
        print_menu()

        choice = input("👉 请选择模型 [1-6/q]: ").strip()

        if choice.lower() == "q":
            print("\n👋 退出程序")
            break

        try:
            model_id = int(choice)
            if model_id not in MODELS:
                print(f"\n❌ 无效选择: {choice}")
                print(f"   请输入 1-6 或 q\n")
                continue
        except ValueError:
            print(f"\n❌ 无效选择: {choice}")
            print(f"   请输入 1-6 或 q\n")
            continue

        model_info = MODELS[model_id]

        # 检查模型文件是否存在
        if not check_model_path(model_info["path"]):
            print(f"\n❌ 模型文件不存在: {model_info['path']}")
            print(f"   请检查路径是否正确\n")
            continue

        # 视觉模型询问是否加载 mmproj
        load_mmproj = False
        if model_info.get("type") == "vision":
            mmproj_path = model_info.get("mmproj", "")
            if check_model_path(mmproj_path):
                mmproj_choice = (
                    input(f"\n👁️ 该模型支持视觉识别，是否加载 mmproj？[y/n]: ")
                    .strip()
                    .lower()
                )
                load_mmproj = mmproj_choice == "y"
                print(
                    f"\n   {'✅ 将加载视觉编码器' if load_mmproj else '💬 纯文本模式'}"
                )
            else:
                print(f"\n⚠️  mmproj 文件不存在，使用纯文本模式")

        # 检查 llama-server
        if not check_llama_server():
            break

        # 运行服务器
        run_server(model_info, load_mmproj)

        print("\n⚠️  服务器已关闭")
        input("\n按回车键返回菜单...")


if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("chcp 65001 >nul")

    print("\n" + "=" * 60)
    print("🤖 模型启动脚本初始化中...")
    print("=" * 60)

    if len(MODELS) == 0:
        print("\n❌ 未配置任何模型！")
        print("   请在脚本中配置 MODELS 字典")
        input("\n按回车键退出...")
        sys.exit(1)

    switch_model()
