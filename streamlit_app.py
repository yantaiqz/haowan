import streamlit as st
import datetime
import time
import pandas as pd

# ==========================================
# 1. 全局配置与 CSS 魔法
# ==========================================
st.set_page_config(page_title="Neal.fun Clone", page_icon="🦕", layout="wide")

# 初始化浇水状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# 注入 CSS
st.markdown("""
<style>
    /* 全局字体 */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {
        font-family: 'Roboto', sans-serif;
        background-color: #f1f2f6; /* 原站背景色 */
    }

    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* -----------------------------------------------------------
       修改点 1: 完美复刻的卡片比例
       原站 CSS: aspect-ratio: 285/107
    ----------------------------------------------------------- */
    .game-card-container {
        /* 强制宽高比 */
        aspect-ratio: 285/107; 
        width: 100%;
        perspective: 1000px;
    }

    .game-card {
        background: white;
        border-radius: 15px; /* 原站圆角 */
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #e7e7e7;
        cursor: pointer;
        padding: 10px;
        position: relative;
        overflow: hidden;
    }

    .game-card:hover {
        transform: scale(1.023); /* 原站悬浮缩放参数 */
        box-shadow: 3px 6px 6px 0 rgba(0,0,0,.11);
    }
    
    .game-card h3 {
        font-size: 1.2rem;
        margin: 0;
        font-weight: 700;
        color: #000;
    }
    
    .game-card p {
        font-size: 0.9rem;
        color: #666;
        margin: 5px 0 0 0;
    }

    .emoji-icon {
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    
    /* -----------------------------------------------------------
       修改点 2: 移植浇水动画 CSS
    ----------------------------------------------------------- */
    
    /* 植物容器 (固定在右下角模拟原站效果) */
    .plant-wrapper {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 100px;
        height: 100px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
    }

    .plant-wrapper:hover {
        transform: scale(1.03);
        transform-origin: bottom;
    }

    /* 植物图片 */
    .plant-img {
        height: 80px;
        z-index: 5;
    }

    /* 浇水动画 (水壶) */
    .watering-can {
        font-size: 50px;
        position: absolute;
        top: -40px;
        left: -40px;
        z-index: 6;
        opacity: 0; /* 默认隐藏 */
        pointer-events: none;
    }

    /* 激活状态下的水壶动画 */
    .animate-water .watering-can {
        /* 移植原站动画参数: .1s ease-in-out 4s forwards (这里为了演示缩短了延迟) */
        animation: watering 1.5s ease-in-out forwards;
    }

    @keyframes watering {
        0% { opacity: 0; transform: rotate(0deg); }
        20% { opacity: 1; transform: rotate(-30deg); } /* 倒水动作 */
        80% { opacity: 1; transform: rotate(-30deg); }
        100% { opacity: 0; transform: rotate(0deg); }
    }

    /* 状态文字气泡 */
    .plant-stat {
        background: #fff;
        border: 1px solid #b5b5b5;
        border-radius: 10px;
        font-size: 14px;
        padding: 7px;
        position: absolute;
        top: -50px;
        width: 140px;
        text-align: center;
        opacity: 0;
        z-index: 5;
        pointer-events: none;
    }
    
    /* 气泡的小三角 */
    .plant-stat:before {
        content: "";
        border-left: 9px solid transparent;
        border-right: 9px solid transparent;
        border-top: 9px solid #b5b5b5;
        position: absolute;
        bottom: -9px;
        left: 50%;
        transform: translateX(-50%);
    }

    /* 激活状态下的文字动画 */
    .animate-water .plant-stat {
        animation: fadeInStat 0.6s ease-in-out 0.5s forwards, 
                   fadeOutStat 0.6s ease-in-out 2.5s forwards;
    }

    @keyframes fadeInStat {
        0% { opacity: 0; transform: translateY(10px) translateX(-50%); }
        to { opacity: 1; transform: translateY(0) translateX(-50%); left: 50%; }
    }

    @keyframes fadeOutStat {
        0% { opacity: 1; transform: translateY(0) translateX(-50%); left: 50%;}
        to { opacity: 0; transform: translateY(-10px) translateX(-50%); left: 50%;}
    }
    
    /* 隐藏Streamlit默认按钮样式以覆盖在植物上 */
    .stButton.plant-btn button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 100px;
        height: 100px;
        opacity: 0; /* 透明按钮 */
        z-index: 10000;
        cursor: pointer;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 状态管理与路由
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 3. 组件：浇水彩蛋 (新功能)
# ==========================================
def render_plant_easter_egg():
    """
    渲染植物和浇水动画。
    利用 CSS class 切换来触发动画。
    """
    
    # 检测是否刚刚点击了浇水
    animation_class = "animate-water" if st.session_state.trigger_water else ""
    
    # 动画 HTML 结构
    html_code = f"""
<div class="plant-wrapper {animation_class}">
    <div class="plant-stat">
        Watered <b>{st.session_state.water_count}</b> times
    </div>
    <div class="watering-can">🚿</div>
    <div class="plant-img" style="font-size:60px;">🪴</div>
</div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    # 创建一个透明的 Streamlit 按钮覆盖在上方，用于触发 Python 逻辑
    st.markdown('<div class="plant-btn">', unsafe_allow_html=True)
    if st.button("Water Plant", key="water_btn"):
        st.session_state.water_count += 1
        st.session_state.trigger_water = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 简单的逻辑：如果触发了动画，下一次刷新时重置触发器，
    # 但为了让用户看到动画，我们不立即重置，而是依赖下一次交互或定时器。
    # 在 Streamlit 中，动画主要由 CSS 控制，Python 只需要负责设置一次状态即可。
    if st.session_state.trigger_water:
        # 这里的逻辑是为了让 Class 在下一次点击前保持，或者你可以选择立即重置
        # 为了演示简单，我们让它保持为 True，下次点击时重新渲染
        pass 

# ==========================================
# 4. 页面内容函数 (Life Stats, Spend Money, Deep Scroll)
# ... (保持原有逻辑不变，为节省篇幅略去部分重复代码，核心在 Home) ...
# ==========================================

def render_life_stats():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("📅 Life Stats")
    col1, _ = st.columns([1, 2])
    with col1:
        birthday = st.date_input("Your Birthday", datetime.date(2000, 1, 1))
    
    now = datetime.datetime.now()
    delta = now - datetime.datetime.combine(birthday, datetime.time())
    seconds = int(delta.total_seconds())
    
    st.markdown(f"## You have been alive for {seconds:,} seconds.")

def render_spend_money():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("💸 Spend Bill Gates' Money")
    st.info("Market is closed. Come back later.")

def render_deep_scroll():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("🌊 The Deep Sea")
    st.markdown("Scroll down...")
    for i in range(0, 1000, 100):
        st.markdown(f"### {i}m depth")
        st.markdown("---")

# ==========================================
# 5. 主页 (应用了新的 Ratio 按钮)
# ==========================================
def render_home():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px;'>Neal.fun Clone</h1>", unsafe_allow_html=True)
    
    # 使用 columns 布局，但内部使用自定义 HTML 卡片
    col1, col2, col3 = st.columns(3)

    # 辅助函数：渲染卡片
    def card(col, title, desc, icon, target_page):
        with col:
            # 外层容器控制比例
            st.markdown(f"""
            <div class="game-card-container">
                <div class="game-card">
                    <div class="emoji-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # -----------------------------------------------------------
            # 修改位置在这里：
            # 将 key=target_page 改为 key=title 或者 key=f"btn_{title}"
            # 这样即使 target_page 相同，只要标题不同，key 就不会冲突
            # -----------------------------------------------------------
            if st.button(f"Play {title}", key=f"btn_{title}", use_container_width=True):
                navigate_to(target_page)
                


    # 渲染三个卡片
    card(col1, "Life Stats", "How long have you lived?", "📅", "life_stats")
    card(col2, "Spend Money", "Spend $100b in 60s", "💸", "spend_money")
    card(col3, "The Deep Sea", "Scroll to the bottom", "🌊", "deep_scroll")

    # 渲染其他行 (示例)
    st.write("")
    st.write("")
    c4, c5, c6 = st.columns(3)
    card(c4, "Draw Circle", "Test your skills", "⭕", "home")
    card(c5, "Space", "Scale of the universe", "🪐", "home")
    card(c6, "Rocks", "Stacking rocks", "🪨", "home")

    # 渲染全局浇水彩蛋
    # render_plant_easter_egg()

# ==========================================
# 6. 程序入口
# ==========================================
if __name__ == "__main__":
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'life_stats':
        render_life_stats()
    elif st.session_state.page == 'spend_money':
        render_spend_money()
    elif st.session_state.page == 'deep_scroll':
        render_deep_scroll()
