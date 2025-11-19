#!/usr/bin/env python3
"""
圣诞树动画部署助手
这个脚本帮助你快速部署3D圣诞树动画
"""

import os
import sys
import subprocess
import webbrowser

def check_requirements():
    """检查必要的文件是否存在"""
    required_files = [
        'streamlit_app.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件都存在")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败")
        return False

def run_local():
    """运行本地版本"""
    print("🚀 启动本地服务器...")
    try:
        # 启动Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.headless', 'true',
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def show_deployment_guide():
    """显示部署指南"""
    guide = """
🎯 部署到互联网的步骤：

1. 📝 创建GitHub账户（如果没有）
   https://github.com

2. 📤 将代码上传到GitHub仓库：
   - 创建新仓库
   - 上传所有文件（streamlit_app.py, requirements.txt, README.md）
   - 确保包含 Procfile（用于某些平台）

3. 🚀 选择部署平台：

   方案A: Streamlit Cloud（最简单）
   - 访问: https://share.streamlit.io
   - 用GitHub登录
   - 选择你的仓库
   - 选择streamlit_app.py作为主文件
   - 点击Deploy

   方案B: Render（免费）
   - 访问: https://render.com
   - 连接GitHub账户
   - 创建新的Web Service
   - 选择你的仓库
   - 启动命令: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0

   方案C: Heroku（需要信用卡验证）
   - 安装Heroku CLI
   - 创建Procfile: echo "web: streamlit run streamlit_app.py --server.port=\\$PORT --server.address=0.0.0.0" > Procfile
   - 部署: heroku create your-app-name && git push heroku main

4. 🔗 分享你的链接
   部署成功后，你会获得一个形如 https://your-app-name.streamlit.app 的链接
   把这个链接分享给朋友即可！

💡 提示: Streamlit Cloud是最简单的方案，推荐新手使用。
"""
    print(guide)

def main():
    """主函数"""
    print("🎄 3D圣诞树动画部署助手")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    print("\n选择操作:")
    print("1. 🚀 运行本地版本（用于测试）")
    print("2. 📚 查看部署指南")
    print("3. 📦 安装依赖包（仅安装，不运行）")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        install_dependencies()
        run_local()
    elif choice == '2':
        show_deployment_guide()
    elif choice == '3':
        install_dependencies()
        print("\n✅ 依赖包安装完成！现在可以运行本地版本了。")
        print("运行命令: streamlit run streamlit_app.py")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()