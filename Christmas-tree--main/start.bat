@echo off
echo 🎄 启动3D圣诞树动画...
echo ========================================

REM 设置Streamlit配置，避免首次启动的邮箱配置
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_SERVER_ENABLE_CORS=false
set STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

REM 启动Streamlit应用
echo 正在启动服务器...
streamlit run streamlit_app.py --server.headless=true --server.port=8501 --server.address=0.0.0.0

echo 服务器已停止
pause