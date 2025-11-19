#!/bin/bash
# 启动圣诞树动画的脚本

echo "🎄 启动3D圣诞树动画..."
echo "========================================"

# 设置Streamlit配置，避免首次启动的邮箱配置
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# 启动Streamlit应用
echo "正在启动服务器..."
streamlit run streamlit_app.py \
    --server.headless=true \
    --server.port=8501 \
    --server.address=0.0.0.0

echo "服务器已停止"