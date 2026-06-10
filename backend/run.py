# -*- coding: utf-8 -*-
"""
TimerFocus 启动入口
    python run.py                -> 开发模式 (Flask dev server)
    python run.py --mode dev     -> 同上
    python run.py --mode desktop -> 桌面模式 (PyWebView 原生窗口)
"""
import os
import sys
import argparse
import threading

# 修复 Windows 控制台 GBK 编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# PyInstaller 需要顶层 import 才能正确分析依赖
try:
    import webview
    HAS_WEBVIEW = True
except ImportError as e:
    HAS_WEBVIEW = False
    WEBVIEW_ERROR = str(e)

# 把后端包加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

app = create_app()

HOST = '127.0.0.1'
PORT = 5000
URL = f'http://{HOST}:{PORT}'


def run_dev():
    """开发模式 - 终端运行，带 debug 热重载"""
    print(f'[TimerFocus] 开发模式')
    print(f'  前端: npm run dev  (localhost:5173)')
    print(f'  后端: {URL}')
    app.run(host=HOST, port=PORT, debug=True)


def run_desktop():
    """桌面模式 - PyWebView 原生窗口"""
    if not HAS_WEBVIEW:
        print(f'[ERROR] 未安装 pywebview: {WEBVIEW_ERROR}')
        print('  请运行: pip install pywebview')
        print('  或使用: python run.py --mode dev')
        sys.exit(1)

    # 在后台线程启动 Flask
    def start_flask():
        app.run(host=HOST, port=PORT, debug=False)

    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    # 创建桌面窗口
    window = webview.create_window(
        title='TimerFocus - 专注计时器',
        url=URL,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        confirm_close=True,
    )

    webview.start(gui='edgechromium' if os.name == 'nt' else None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TimerFocus 启动器')
    parser.add_argument(
        '--mode', '-m',
        choices=['dev', 'desktop'],
        default='desktop' if getattr(sys, 'frozen', False) else 'dev',
        help='启动模式: dev=开发模式, desktop=桌面模式'
    )
    args = parser.parse_args()

    if args.mode == 'desktop':
        run_desktop()
    else:
        run_dev()
