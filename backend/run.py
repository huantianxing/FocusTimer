import os
import sys

# 把项目根目录加入 Python 识别路径，防止找不到文件
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app # 从 app 文件夹导入创建app的函数

# 调用create_app，拿到app，运行app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)