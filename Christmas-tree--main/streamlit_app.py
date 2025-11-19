import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from math import pi, sin, cos, sqrt
import tempfile
import io
import base64

# 设置页面配置
st.set_page_config(
    page_title="3D圣诞树动画",
    page_icon="🎄",
    layout="wide"
)

# CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FFD93D;
        font-size: 3em;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .description {
        text-align: center;
        font-size: 1.2em;
        color: #E0E0E0;
        margin-bottom: 30px;
    }
    .controls {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎄 3D圣诞树动画 🎄</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">一个精美的3D圣诞树动画，带有雪花、装饰球和旋转的心形</p>', unsafe_allow_html=True)

# 参数控制
with st.sidebar:
    st.header("控制面板")
    
    # 粒子数量控制
    N_tree = st.slider("树粒子数量", 1000, 10000, 6000, 1000)
    N_ground = st.slider("地面粒子数量", 1000, 8000, 3500, 500)
    N_snow = st.slider("雪花数量", 500, 3000, 1500, 250)
    N_decorations = st.slider("装饰球数量", 100, 1000, 400, 50)
    
    # 动画控制
    animation_speed = st.slider("动画速度", 10, 100, 40, 10)
    show_wireframe = st.checkbox("显示线框", False)
    
    # 颜色主题
    theme = st.selectbox("颜色主题", 
                        ["经典绿色", "冬季蓝", "温暖橙", "神秘紫"])

# ==============================
# 主题颜色配置
# ==============================
def get_theme_colors(theme_name):
    themes = {
        "经典绿色": {
            "background": "#0a0a2a",
            "ground": "white",
            "snow": "white",
            "text": "#FFD93D"
        },
        "冬季蓝": {
            "background": "#1a1a3a",
            "ground": "#E0F6FF",
            "snow": "#E0F6FF",
            "text": "#87CEEB"
        },
        "温暖橙": {
            "background": "#2a1a0a",
            "ground": "#FFF8DC",
            "snow": "#FFF8DC",
            "text": "#FFB347"
        },
        "神秘紫": {
            "background": "#2a0a2a",
            "ground": "#F0E6FF",
            "snow": "#F0E6FF",
            "text": "#DDA0DD"
        }
    }
    return themes.get(theme_name, themes["经典绿色"])

# ==============================
# 生成函数
# ==============================
def generate_tree(n=6000):
    z = np.random.uniform(0, 1, n)
    radius = (1 - z)**1.5 * 3.5 + np.random.rand(n) * 0.4
    theta = np.random.uniform(0, 2*np.pi, n)
    
    x = radius * np.cos(theta) + (np.random.rand(n) - 0.5) * 0.2
    y = radius * np.sin(theta) + (np.random.rand(n) - 0.5) * 0.2
    z = z * 10 - 0.5
    
    return x, y, z

def generate_decorations(tree_x, tree_y, tree_z, n=400):
    indices = np.random.choice(len(tree_x), n, replace=False)
    deco_x = tree_x[indices] * 1.1
    deco_y = tree_y[indices] * 1.1
    deco_z = tree_z[indices]
    
    colors = np.random.choice(['#FF6B6B', '#FFD93D', '#4ECDC4', '#C7C7C7', '#FF69B4', '#98FB98'], n)
    sizes = np.random.uniform(10, 18, n)
    
    return deco_x, deco_y, deco_z, colors, sizes

def generate_3d_heart(n=1200, scale=0.5, z_top=10.2):
    R = 1.0
    r = R * 0.382
    outer_angles = np.linspace(0, 2*np.pi, 6)[:-1]
    inner_angles = outer_angles + np.pi/5
    
    outer_x = R * np.cos(outer_angles)
    outer_z = R * np.sin(outer_angles)
    inner_x = r * np.cos(inner_angles)
    inner_z = r * np.sin(inner_angles)
    
    star_x_2d = np.empty(10)
    star_z_2d = np.empty(10)
    star_x_2d[0::2] = outer_x
    star_x_2d[1::2] = inner_x
    star_z_2d[0::2] = outer_z
    star_z_2d[1::2] = inner_z
    
    pts_x = []
    pts_y = []
    pts_z = []
    thickness = 0.12
    
    for _ in range(n):
        idx = np.random.randint(0, 10)
        next_idx = (idx + 1) % 10
        cx = 0
        cz = 0
        
        a = np.random.rand()
        b = np.random.rand()
        if a + b > 1:
            a = 1 - a
            b = 1 - b
        
        x = cx + a * star_x_2d[idx] + b * star_x_2d[next_idx]
        z = cz + a * star_z_2d[idx] + b * star_z_2d[next_idx]
        y = np.random.uniform(-thickness, thickness)
        
        pts_x.append(x)
        pts_y.append(y)
        pts_z.append(z)
    
    pts_x = np.array(pts_x)
    pts_y = np.array(pts_y)
    pts_z = np.array(pts_z)
    
    pts_x *= scale
    pts_y *= scale
    pts_z *= scale
    
    pts_x += np.random.normal(0, 0.01, n)
    pts_y += np.random.normal(0, 0.01, n)
    pts_z += np.random.normal(0, 0.01, n)
    
    min_z = np.min(pts_z)
    pts_z = pts_z - min_z + z_top
    
    return pts_x, pts_y, pts_z

def generate_ground(n=3500):
    r = np.sqrt(np.random.rand(n)) * 8
    theta = np.random.rand(n) * 2 * np.pi
    
    wave1 = np.sin(r * 1.2) * 0.2
    wave2 = np.sin(theta * 3 + r * 1.5) * 0.1
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = wave1 + wave2 - 1
    
    return x, y, z

def generate_snow(n=1500):
    x = np.random.uniform(-11, 11, n)
    y = np.random.uniform(-11, 11, n)
    z = np.random.uniform(0, 12, n)
    sizes = np.random.uniform(3, 5, n)
    
    return np.column_stack([x, y, z]), sizes

def create_tree_colors(z, theme_colors):
    normalized_z = (z - z.min()) / (z.max() - z.min())
    colors = []
    
    # 根据主题调整颜色
    base_green = [0.2, 0.6, 0.2] if theme_colors["background"] == "#0a0a2a" else [0.3, 0.7, 0.3]
    light_green = [0.4, 0.8, 0.4] if theme_colors["background"] == "#0a0a2a" else [0.5, 0.9, 0.5]
    
    for z_val in z:
        t = (z_val - z.min()) / (z.max() - z.min())
        r = base_green[0] * (1 - t) + light_green[0] * t
        g = base_green[1] * (1 - t) + light_green[1] * t
        b = base_green[2] * (1 - t) + light_green[2] * t
        colors.append([r, g, b])
    return colors

# ==============================
# 生成和显示动画
# ==============================
def create_christmas_tree():
    # 获取主题颜色
    theme_colors = get_theme_colors(theme)
    
    # 生成所有粒子
    tree_x, tree_y, tree_z = generate_tree(N_tree)
    deco_x, deco_y, deco_z, deco_colors, deco_sizes = generate_decorations(tree_x, tree_y, tree_z, N_decorations)
    heart_x, heart_y, heart_z = generate_3d_heart(n=800, scale=0.7, z_top=9.6)
    ground_x, ground_y, ground_z = generate_ground(N_ground)
    snow_positions, snow_sizes = generate_snow(N_snow)
    
    # 存储原始坐标
    heart_original = np.vstack([heart_x, heart_y, heart_z])
    
    # 创建图形
    fig = plt.figure(figsize=(12, 14))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(theme_colors["background"])
    fig.patch.set_facecolor(theme_colors["background"])
    ax.set_axis_off()
    
    # 设置坐标范围
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-2, 8)
    
    # 初始视角
    ax.view_init(25, -30)
    
    # 创建颜色
    tree_colors = create_tree_colors(tree_z, theme_colors)
    
    # 创建散点图
    tree_scatter = ax.scatter(tree_x, tree_y, tree_z, s=4, c=tree_colors, alpha=0.9, linewidths=0)
    deco_scatter = ax.scatter(deco_x, deco_y, deco_z, s=deco_sizes, c=deco_colors, alpha=0.9)
    
    # 心形
    heart_colors_array = np.ones((len(heart_x), 4))
    heart_colors_array[:, 0] = 1.0
    heart_colors_array[:, 1] = 0.84
    heart_colors_array[:, 2] = 0.0
    
    dist_center = np.sqrt(heart_x**2 + (heart_z - 10.2)**2 + heart_y**2)
    heart_alpha = 0.8 * np.exp(- (dist_center**2) / (2*(0.5**2))) + 0.3
    heart_colors_array[:, 3] = np.clip(heart_alpha, 0.2, 0.95)
    
    heart_scatter = ax.scatter(heart_x, heart_y, heart_z, s=4, c=heart_colors_array)
    
    # 地面和雪花
    ground_scatter = ax.scatter(ground_x, ground_y, ground_z, s=2, color=theme_colors["ground"], alpha=0.7, linewidths=0)
    snow_scatter = ax.scatter(snow_positions[:, 0], snow_positions[:, 1], snow_positions[:, 2], 
                             s=snow_sizes, color=theme_colors["snow"], alpha=0.8)
    
    # 添加文字
    ax.text2D(0.35, 0.25, "Merry Christmas", transform=ax.transAxes, color=theme_colors["text"], 
              fontsize=28, fontweight='bold', fontfamily='Comic Sans MS')
    
    # 星星背景
    star_x = np.random.uniform(-10, 10, 80)
    star_y = np.random.uniform(-10, 10, 80)  
    star_z = np.random.uniform(8, 12, 80)
    ax.scatter(star_x, star_y, star_z, s=np.random.uniform(1, 3, 80), color=theme_colors["snow"], alpha=0.6)
    
    # 动画更新函数
    def rotation_matrix_z(deg):
        th = np.deg2rad(deg)
        c, s = np.cos(th), np.sin(th)
        return np.array([[c, -s, 0],
                         [s,  c, 0],
                         [0,  0, 1]])
    
    heart_initial_sizes = np.full(len(heart_x), 4)
    
    def update(frame):
        # 雪花飘落
        snow_positions[:, 2] -= 0.07
        reset_mask = snow_positions[:, 2] < -2
        reset_count = np.sum(reset_mask)
        if reset_count > 0:
            snow_positions[reset_mask, 2] = 12
            snow_positions[reset_mask, 0] = np.random.uniform(-11, 11, reset_count)
            snow_positions[reset_mask, 1] = np.random.uniform(-11, 11, reset_count)
        snow_scatter._offsets3d = (snow_positions[:, 0], snow_positions[:, 1], snow_positions[:, 2])
        
        # 树闪烁效果
        tree_alpha = 0.85 + 0.1 * np.sin(frame * 0.2)
        tree_scatter.set_alpha(tree_alpha)
        
        # 心形旋转
        R = rotation_matrix_z(frame * 0.1)
        heart_rotated = R @ heart_original
        heart_scatter._offsets3d = (heart_rotated[0,:], heart_rotated[1,:], heart_rotated[2,:])
        
        # 心形脉动效果
        pulse = 0.9 + 0.1 * np.sin(frame * 0.15)
        current_sizes = heart_initial_sizes * pulse
        heart_scatter.set_sizes(current_sizes)
        
        # 心形颜色闪烁
        heart_alpha_dynamic = 0.7 + 0.3 * np.sin(frame * 0.12)
        current_colors = heart_colors_array.copy()
        current_colors[:, 3] = np.clip(heart_colors_array[:, 3] * heart_alpha_dynamic, 0.2, 0.95)
        heart_scatter.set_color(current_colors)
        
        # 装饰球闪烁
        deco_alpha = 0.8 + 0.2 * np.sin(frame * 0.25)
        deco_scatter.set_alpha(deco_alpha)
        
        # 旋转视角
        elev = 25 + 1.5 * np.sin(frame * 0.04)
        azim = -30 + frame * 0.08
        ax.view_init(elev, azim)
        
        return []
    
    # 创建动画
    try:
        ani = FuncAnimation(fig, update, frames=1000, interval=animation_speed, blit=False, repeat=True)
        
        # 保存动画到临时文件
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
            ani.save(tmp_file.name, writer='pillow', fps=25, dpi=80)
            
            # 显示动画
            st.image(tmp_file.name, caption="🎄 3D圣诞树动画", use_column_width=True)
            
        plt.close(fig)
        
    except Exception as e:
        st.error(f"生成动画时出错: {e}")
        plt.close(fig)

# 主界面
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎅 生成圣诞树动画", type="primary", use_container_width=True):
        with st.spinner("正在生成圣诞树动画..."):
            create_christmas_tree()

# 添加一些信息
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 30px;">
<h3 style="color: #FFD93D;">🎁 功能特点</h3>
<ul style="color: #E0E0E0;">
<li>🌲 3D立体圣诞树，带有丰富的绿色渐变效果</li>
<li>✨ 动态雪花飘落效果</li>
<li>🎈 多彩装饰球随机分布</li>
<li>💝 顶部旋转的金色心形</li>
<li>🌟 闪烁的星星背景</li>
<li>🎨 多种颜色主题可选</li>
<li>⚙️ 可调节粒子数量和动画参数</li>
</ul>
</div>
""", unsafe_allow_html=True)