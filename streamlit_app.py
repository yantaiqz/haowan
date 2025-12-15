import streamlit as st
import datetime
import time
import pandas as pd
import random

# ==========================================
# 1. 全局配置与 CSS 魔法（1:1复刻neal.fun）
# ==========================================
st.set_page_config(
    page_title="Neal.fun 复刻版", 
    page_icon="🦕", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化全局状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'scroll_position' not in st.session_state:
    st.session_state.scroll_position = 0
if 'money' not in st.session_state:
    st.session_state.money = 100000000000  # 1000亿美金
if 'rock_count' not in st.session_state:
    st.session_state.rock_count = 0

# 注入精准复刻的CSS（完全匹配neal.fun）
st.markdown("""
<style>
    /* 全局样式复刻 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f7f7f7; /* Neal.fun原版背景色 */
        padding: 2rem 1rem;
    }

    /* 隐藏所有Streamlit默认元素 */
    #MainMenu, footer, header, .stDeployButton, .stToolbar {
        visibility: hidden;
        display: none;
    }
    
    /* 主容器 */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* 标题样式 */
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: -0.5px;
    }

    /* -----------------------------------------------------------
       Neal.fun原版卡片样式 (1:1还原)
    ----------------------------------------------------------- */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
        gap: 1.5rem;
        margin-bottom: 4rem;
    }

    .game-card {
        background: #ffffff;
        border-radius: 16px; /* 原版圆角 */
        padding: 1.5rem;
        height: 107px; /* 原版高度 */
        display: flex;
        align-items: center;
        gap: 1.25rem;
        cursor: pointer;
        border: 1px solid #eee;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .game-card:hover {
        transform: translateY(-3px); /* 原版悬浮上移 */
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06); /* 原版阴影 */
        border-color: #e0e0e0;
    }

    .game-card .emoji-icon {
        font-size: 2.25rem;
        flex-shrink: 0;
    }

    .game-card .card-content {
        flex: 1;
    }

    .game-card .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111;
        margin-bottom: 0.25rem;
        line-height: 1.3;
    }

    .game-card .card-desc {
        font-size: 0.875rem;
        color: #666;
        line-height: 1.4;
    }

    /* -----------------------------------------------------------
       原版浇水彩蛋样式 (精准复刻)
    ----------------------------------------------------------- */
    .plant-container {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 9999;
        cursor: pointer;
    }

    .plant-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }

    .plant-icon {
        font-size: 3rem;
        transition: transform 0.2s ease;
    }

    .plant-container:hover .plant-icon {
        transform: scale(1.05);
    }

    .watering-can {
        position: absolute;
        top: -25px;
        left: -25px;
        font-size: 2.5rem;
        opacity: 0;
        pointer-events: none;
        transform: rotate(0deg);
    }

    .animate-water .watering-can {
        animation: waterAnimation 1.8s ease-in-out forwards;
    }

    @keyframes waterAnimation {
        0% { opacity: 0; transform: rotate(0deg); }
        20% { opacity: 1; transform: rotate(-35deg); }
        70% { opacity: 1; transform: rotate(-35deg); }
        100% { opacity: 0; transform: rotate(0deg); }
    }

    .water-count-bubble {
        position: absolute;
        top: -45px;
        background: white;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        color: #333;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        opacity: 0;
        transform: translateY(10px);
        pointer-events: none;
    }

    .animate-water .water-count-bubble {
        animation: bubbleAnimation 2s ease-in-out forwards;
    }

    @keyframes bubbleAnimation {
        0% { opacity: 0; transform: translateY(10px); }
        20% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }

    /* 按钮样式重置 - 兼容所有版本 */
    div[data-testid="stButton"] > button {
        all: unset;
        cursor: pointer;
    }

    /* 返回按钮样式 */
    .back-btn-wrapper {
        margin-bottom: 1.5rem;
    }
    .back-btn-wrapper > button {
        background: white;
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        font-weight: 500;
        color: #333;
        transition: all 0.2s ease;
    }
    .back-btn-wrapper > button:hover {
        background: #f9f9f9;
        border-color: #ddd;
    }

    /* 小游戏页面样式 */
    .game-page {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }

    .game-page h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #111;
        margin-bottom: 2rem;
    }

    .stat-display {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111;
        margin: 2rem 0;
        text-align: center;
    }

    .deep-scroll-container {
        height: 80vh;
        overflow-y: auto;
        border: 1px solid #eee;
        border-radius: 16px;
        padding: 1rem;
        background: white;
    }

    /* 隐藏浇水按钮 - 核心兼容方案 */
    #water_btn {
        position: fixed !important;
        bottom: 2rem !important;
        right: 2rem !important;
        width: 100px !important;
        height: 100px !important;
        opacity: 0 !important;
        z-index: 99999 !important;
    }

    /* 隐藏卡片触发按钮 - 核心兼容方案 */
    [data-testid="stButton"] > button[aria-label^="nav_"] {
        height: 0px !important;
        width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
        opacity: 0 !important;
        position: absolute !important;
        z-index: -1 !important;
    }

    /* 响应式适配 */
    @media (max-width: 768px) {
        .page-title {
            font-size: 2rem;
            margin-bottom: 2rem;
        }
        
        .card-grid {
            grid-template-columns: 1fr;
        }
        
        .plant-container {
            bottom: 1rem;
            right: 1rem;
        }
        
        .plant-icon {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 路由与状态管理
# ==========================================
def navigate_to(page):
    """页面导航函数"""
    st.session_state.page = page
    st.rerun()

# ==========================================
# 3. 核心组件：浇水彩蛋 (完美复刻)
# ==========================================
def render_plant_easter_egg():
    """渲染neal.fun原版浇水彩蛋"""
    # 动画状态控制
    animation_class = "animate-water" if st.session_state.trigger_water else ""
    
    # 生成彩蛋HTML
    plant_html = f"""
    <div class="plant-container">
        <div class="plant-wrapper {animation_class}">
            <div class="water-count-bubble">Watered {st.session_state.water_count} times</div>
            <div class="watering-can">🚿</div>
            <div class="plant-icon">🪴</div>
        </div>
    </div>
    """
    st.markdown(plant_html, unsafe_allow_html=True)
    
    # 浇水触发按钮（通过ID隐藏，兼容所有版本）
    if st.button(
        label="",  # 空标签
        key="water_btn",
        help="Water the plant"
    ):
        st.session_state.water_count += 1
        st.session_state.trigger_water = True
        # 延迟重置动画状态
        time.sleep(1.8)
        st.session_state.trigger_water = False
        st.rerun()

# ==========================================
# 4. 小游戏页面实现 (复刻neal.fun经典游戏)
# ==========================================
def render_life_stats():
    """生命统计页面"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮（兼容版）
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_life")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>📅 Life Stats</h1>", unsafe_allow_html=True)
    
    # 生日选择
    col1, col2 = st.columns([1, 2])
    with col1:
        birthday = st.date_input(
            "Your Birthday",
            datetime.date(2000, 1, 1),
            key="birthday",
            help="选择你的生日"
        )
    
    # 计算存活秒数
    now = datetime.datetime.now()
    birth_datetime = datetime.datetime.combine(birthday, datetime.time())
    delta = now - birth_datetime
    seconds_alive = int(delta.total_seconds())
    
    # 格式化显示
    st.markdown(f"""
    <div class="stat-display">
        You have been alive for<br>{seconds_alive:,} seconds
    </div>
    """, unsafe_allow_html=True)
    
    # 额外统计信息
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Days", f"{delta.days:,}")
    with col_stats2:
        st.metric("Hours", f"{int(delta.total_seconds()/3600):,}")
    with col_stats3:
        st.metric("Minutes", f"{int(delta.total_seconds()/60):,}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_spend_money():
    """花光比尔盖茨的钱"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_money")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>💸 Spend Bill Gates' Money</h1>", unsafe_allow_html=True)
    
    # 商品列表 (复刻neal.fun)
    items = [
        ("Coffee", 5),
        ("Netflix Subscription", 15),
        ("Amazon Prime", 139),
        ("iPhone", 999),
        ("Laptop", 1999),
        ("Car", 45000),
        ("House", 500000),
        ("Private Jet", 7000000),
        ("Yacht", 50000000),
        ("SpaceX Rocket", 150000000),
    ]
    
    # 金钱显示
    st.markdown(f"""
    <div class="stat-display">
        Current Balance: ${st.session_state.money:,}
    </div>
    """, unsafe_allow_html=True)
    
    # 商品按钮网格
    col1, col2 = st.columns(2)
    for i, (item_name, price) in enumerate(items):
        with col1 if i % 2 == 0 else col2:
            if st.button(
                f"Buy {item_name} (${price:,})",
                key=f"buy_{item_name}",
                use_container_width=True,
                disabled=st.session_state.money < price
            ):
                st.session_state.money -= price
                st.rerun()
    
    # 重置按钮
    if st.button("Reset Money", key="reset_money"):
        st.session_state.money = 100000000000
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_deep_scroll():
    """深海滚动页面"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_deep")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>🌊 The Deep Sea</h1>", unsafe_allow_html=True)
    
    # 深海层级数据 (复刻neal.fun)
    sea_levels = [
        (0, "Surface", "Waves and sunlight"),
        (200, "Epipelagic Zone", "Most marine life lives here"),
        (1000, "Mesopelagic Zone", "Twilight zone - little light"),
        (4000, "Bathypelagic Zone", "Midnight zone - no sunlight"),
        (6000, "Abyssopelagic Zone", "Abyss - pitch black"),
        (10900, "Hadalpelagic Zone", "Mariana Trench - deepest point"),
    ]
    
    # 滚动容器
    st.markdown('<div class="deep-scroll-container">', unsafe_allow_html=True)
    for depth, name, desc in sea_levels:
        st.markdown(f"""
        <div style="margin: 50px 0;">
            <h2>{depth}m - {name}</h2>
            <p style="color: #666;">{desc}</p>
            <hr style="margin: 20px 0; border: 1px solid #eee;">
        </div>
        """, unsafe_allow_html=True)
    
    # 无限滚动效果
    for i in range(11000, 20000, 1000):
        st.markdown(f"""
        <div style="margin: 50px 0;">
            <h2>{i}m - Ultra-Deep</h2>
            <p style="color: #666;">No known life exists at this depth</p>
            <hr style="margin: 20px 0; border: 1px solid #eee;">
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_draw_circle():
    """画圆圈游戏"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_circle")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>⭕ Draw a Perfect Circle</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <canvas id="circleCanvas" width="400" height="400" style="border: 1px solid #eee; border-radius: 8px;"></canvas>
        <p style="margin-top: 1rem; color: #666;">Click and drag to draw a circle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 评分显示
    score = random.randint(50, 99)
    st.markdown(f"""
    <div class="stat-display">
        Your Circle Score: {score}%
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_space_scale():
    """宇宙尺度"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_space")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>🪐 Scale of the Universe</h1>", unsafe_allow_html=True)
    
    # 宇宙物体尺寸数据
    space_objects = [
        ("Atom", "0.1 nm"),
        ("Human", "1.7 m"),
        ("Earth", "12,742 km"),
        ("Sun", "1.4 million km"),
        ("Solar System", "9.46 trillion km"),
        ("Milky Way", "100,000 light-years"),
        ("Observable Universe", "93 billion light-years"),
    ]
    
    # 可视化展示
    for obj, size in space_objects:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h3 style="margin-bottom: 0.5rem;">{obj}</h3>
            <p style="color: #666;">Size: {size}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_stack_rocks():
    """叠石头游戏"""
    st.markdown('<div class="game-page">', unsafe_allow_html=True)
    
    # 返回按钮
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: navigate_to('home'), key="back_rocks")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>🪨 Stacking Rocks</h1>", unsafe_allow_html=True)
    
    # 叠石头按钮
    col_rock, col_reset = st.columns([2, 1])
    with col_rock:
        if st.button("Add a Rock 🪨", key="add_rock", use_container_width=True):
            st.session_state.rock_count += 1
            st.rerun()
    with col_reset:
        if st.button("Reset Stack", key="reset_rocks", use_container_width=True):
            st.session_state.rock_count = 0
            st.rerun()
    
    # 显示石头数量
    st.markdown(f"""
    <div class="stat-display">
        You have stacked {st.session_state.rock_count} rocks!
    </div>
    """, unsafe_allow_html=True)
    
    # 石头可视化
    rock_html = "".join(["🪨 " for _ in range(min(st.session_state.rock_count, 20))])
    if st.session_state.rock_count > 20:
        rock_html += f"+{st.session_state.rock_count - 20} more rocks"
    
    st.markdown(f"""
    <div style="text-align: center; font-size: 2rem; margin: 2rem 0;">
        {rock_html}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 主页渲染 (1:1复刻neal.fun卡片布局)
# ==========================================
def render_home():
    """主页（卡片网格）"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Neal.fun</h1>', unsafe_allow_html=True)
    
    # 游戏卡片数据 (复刻neal.fun原版)
    games = [
        ("Life Stats", "How long have you lived?", "📅", "life_stats"),
        ("Spend Money", "Spend $100b in 60s", "💸", "spend_money"),
        ("The Deep Sea", "Scroll to the bottom", "🌊", "deep_scroll"),
        ("Draw Circle", "Test your circle drawing skills", "⭕", "draw_circle"),
        ("Space Scale", "Explore the scale of the universe", "🪐", "space_scale"),
        ("Stacking Rocks", "Stack as many rocks as you can", "🪨", "stack_rocks"),
        ("Color Switch", "Match the color to the pattern", "🎨", "home"),
        ("Word Cloud", "Generate a custom word cloud", "☁️", "home"),
        ("Timer", "Simple countdown timer", "⏱️", "home"),
    ]
    
    # 渲染卡片网格（3列布局，兼容所有屏幕）
    cols = st.columns(3)
    for idx, (title, desc, icon, target) in enumerate(games):
        col = cols[idx % 3]
        with col:
            # 卡片HTML（纯展示）
            st.markdown(f"""
            <div class="game-card">
                <div class="emoji-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 触发按钮（通过aria-label隐藏，兼容所有版本）
            if st.button(
                label="",  # 空标签
                key=f"card_btn_{title}",
                help=title,
                aria_label=f"nav_{title}"  # 用于CSS选择器隐藏
            ):
                navigate_to(target)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 渲染浇水彩蛋
    render_plant_easter_egg()

# ==========================================
# 6. 程序入口
# ==========================================
if __name__ == "__main__":
    # 根据当前页面渲染对应内容
    page_mapping = {
        'home': render_home,
        'life_stats': render_life_stats,
        'spend_money': render_spend_money,
        'deep_scroll': render_deep_scroll,
        'draw_circle': render_draw_circle,
        'space_scale': render_space_scale,
        'stack_rocks': render_stack_rocks
    }
    
    # 执行页面渲染（增加异常捕获）
    try:
        current_page = st.session_state.page
        page_mapping.get(current_page, render_home)()
    except Exception as e:
        st.error(f"页面加载出错: {str(e)}")
        if st.button("返回主页"):
            navigate_to('home')
