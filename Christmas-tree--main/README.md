# 🎄 3D圣诞树动画

一个精美的3D圣诞树动画程序，现在已经转换为可以分享的网页版本！

## ✨ 功能特点

- 🌲 **3D立体圣诞树**：带有丰富的绿色渐变效果
- ❄️ **动态雪花**：随机飘落的雪花效果
- 🎈 **多彩装饰球**：随机分布的彩色装饰
- 💝 **旋转心形**：顶部的金色心形装饰
- 🌟 **星空背景**：闪烁的星星
- 🎨 **多种主题**：经典绿色、冬季蓝、温暖橙、神秘紫
- ⚙️ **参数调节**：可自定义粒子数量和动画速度

## 🚀 部署选项

### 选项1：Streamlit Cloud（推荐，最简单）

1. 将代码上传到GitHub仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接你的GitHub账户
4. 选择仓库和`streamlit_app.py`文件
5. 点击"Deploy!"
6. 获得分享链接

**详细步骤**：
1. 创建GitHub仓库并上传所有文件
2. 访问 https://share.streamlit.io
3. 使用GitHub登录
4. 点击"New app"
5. 选择你的仓库和`streamlit_app.py`
6. 点击"Deploy"

### 选项2：本地运行和分享

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
streamlit run streamlit_app.py

# 3. 访问 http://localhost:8501
```

### 选项3：部署到其他云平台

#### Heroku部署：
1. 安装Heroku CLI
2. 创建`Procfile`文件：`web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
3. 部署：
```bash
heroku create your-app-name
git push heroku main
```

#### Vercel部署：
1. 安装Vercel CLI
2. 创建配置文件
3. 部署：
```bash
vercel --prod
```

#### Render部署：
1. 连接GitHub仓库
2. 选择Web Service
3. 设置启动命令：`streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

## 📁 文件说明

- `streamlit_app.py` - 主程序文件
- `requirements.txt` - Python依赖
- `santa1.py` - 原始程序
- `README.md` - 说明文档

## 🎮 使用方法

1. 访问你的应用链接
2. 在左侧面板调整参数：
   - 调整粒子数量
   - 选择颜色主题
   - 设置动画速度
3. 点击"生成圣诞树动画"
4. 享受你的专属圣诞树！

## 🛠️ 技术栈

- **Streamlit** - 网页应用框架
- **NumPy** - 数值计算
- **Matplotlib** - 3D图形和动画
- **Pillow** - 图像处理

## 🌟 预览效果

应用包含：
- 实时3D动画
- 交互式控制面板
- 美观的用户界面
- 移动端适配

## 📝 许可证

MIT License - 可自由使用和修改

## 🎉 分享你的作品

部署成功后，你将获得一个像这样的分享链接：
`https://your-app-name.streamlit.app`

把这个链接分享给朋友，他们就能看到你的3D圣诞树动画了！

---

**节日快乐！🎅✨**