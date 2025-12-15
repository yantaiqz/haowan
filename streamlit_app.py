import streamlit as st
import datetime
import time
import random

# ==========================================
# 1. 全局配置与状态初始化
# ==========================================
st.set_page_config(
    page_title="Neal.fun Clone",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化 Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 游戏状态：花光首富的钱
if 'money' not in st.session_state:
    st.session_state.total_money = 100000000000
    st.session_state.balance = 100000000000
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# 游戏状态：叠石头
if 'rock_count' not in st.session_state:
    st.session_state.rock_count = 0

# 彩蛋状态：浇水
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# ==========================================
# 2. 核心 CSS 样式 (1:1匹配Neal.fun)
# ==========================================
st.markdown("""
<style>
    /* 引入字体 Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* 全局样式 - 白色背景 */
    .stApp {
        background-color: #FFFFFF !important; /* 纯白背景 */
        font-family: 'Inter', sans-serif;
        color: #111827;
        padding: 0 2rem;
    }

    /* 隐藏无关元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* 标题样式 */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        letter-spacing: -1px;
    }

    /* 副标题样式 */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #6B7280;
        margin: -20px 0 40px 0;
        font-weight: 400;
    }

    /* ----------------------
       Neal.fun 卡片样式 (1:1尺寸)
       ---------------------- */
    .neal-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px 16px;
        height: 107px; /* Neal.fun原版卡片高度 */
        width: 100%;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: row; /* 横向布局 */
        align-items: center;
        text-align: left;
        position: relative;
        gap: 16px;
        cursor: pointer;
    }

    /* 悬浮动效 - 匹配neal.fun */
    .neal-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border-color: #D1D5DB;
        z-index: 1;
    }

    .card-icon { 
        font-size: 32px; 
        flex-shrink: 0;
    }
    .card-content {
        flex: 1;
    }
    .card-title { 
        font-size: 18px; 
        font-weight: 700; 
        margin-bottom: 4px; 
        color: #111; 
        line-height: 1.2;
    }
    .card-desc { 
        font-size: 14px; 
        color: #6B7280; 
        line-height: 1.4;
    }

    /* ----------------------
       按钮样式 (1:1匹配neal.fun)
       ---------------------- */
    /* 全局按钮重置 */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        border: 1px solid #E5E7EB !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        transition: all 0.15s ease !important;
        height: auto !important;
        line-height: 1.5 !important;
    }

    /* 按钮悬浮效果 */
    .stButton > button:hover {
        background: #F9FAFB !important;
        border-color: #D1D5DB !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }

    /* 主要按钮样式 */
    .primary-btn > button {
        background: #3B82F6 !important;
        color: white !important;
        border-color: #3B82F6 !important;
    }
    .primary-btn > button:hover {
        background: #2563EB !important;
        border-color: #2563EB !important;
    }

    /* 右上角按钮容器 */
    .top-right-btn {
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 999;
    }

    /* 底部区域样式 */
    .footer-area {
        max-width: 1200px;
        margin: 60px auto 40px;
        padding: 40px 0;
        border-top: 1px solid #E5E7EB;
    }

    .footer-links {
        display: flex;
        flex-wrap: wrap;
        gap: 24px;
        margin-top: 24px;
        align-items: center;
    }

    .footer-text {
        color: #6B7280;
        font-size: 14px;
        line-height: 1.6;
        max-width: 600px;
    }

    /* ----------------------
       功能性 CSS
       ---------------------- */
    /* 余额悬浮条 */
    .money-bar {
        position: fixed; top: 0; left: 0; width: 100%;
        background: #2ecc71; color: white;
        text-align: center; padding: 15px;
        font-size: 24px; font-weight: 800;
        z-index: 999; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 返回按钮 */
    .back-btn-area { margin-bottom: 20px; }
    
    /* 浇水彩蛋 */
    .plant-container {
        position: fixed; bottom: 20px; right: 20px;
        text-align: center; z-index: 999;
    }
    .water-bubble {
        background: white; padding: 8px 12px; border-radius: 12px;
        font-size: 14px; font-weight: 700;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 8px; opacity: 0; transition: opacity 0.3s;
    }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 60px; cursor: pointer; transition: transform 0.2s; }
    .plant-emoji:hover { transform: scale(1.1); }
    
    /* 深海背景 */
    .deep-sea-box {
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        color: white;
        transition: background-color 0.5s ease;
        min-height: 400px;
        display: flex; flex-direction: column; justify-content: center;
    }

    /* 响应式适配 */
    @media (max-width: 768px) {
        .top-right-btn {
            position: static;
            margin-bottom: 20px;
            text-align: right;
        }
        .footer-links {
            flex-direction: column;
            align-items: flex-start;
            gap: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 路由控制
# ==========================================
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 4. 右上角按钮组件
# ==========================================
def render_top_right_button():
    """渲染右上角 Get New Posts 按钮"""
    st.markdown('<div class="top-right-btn">', unsafe_allow_html=True)
    st.button("Get new posts", key="top_btn", help="Subscribe to updates")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 底部组件 (匹配neal.fun)
# ==========================================
def render_footer():
    """渲染底部区域"""
    st.markdown("""
    <div class="footer-area">
        <h3>About this site</h3>
        <p class="footer-text">
            This is a collection of silly little projects I've made over the years. 
            None of them are particularly useful, but they're all fun to play with.
        </p>
        <div class="footer-links">
            <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration: none;">
                <button style="font-family: Inter; border-radius: 8px; padding: 8px 16px; border: 1px solid #E5E7EB; background: #FFF; color: #111; cursor: pointer;">
                    Newsletter 📰
                </button>
            </a>
            <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration: none;">
                <button style="font-family: Inter; border-radius: 8px; padding: 8px 16px; border: 1px solid #E5E7EB; background: #FFF; color: #111; cursor: pointer;">
                    Twitter 🐦
                </button>
            </a>
            <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration: none;">
                <button style="font-family: Inter; border-radius: 8px; padding: 8px 16px; border: 1px solid #E5E7EB; background: #FFF; color: #111; cursor: pointer;">
                    Buy me a coffee ☕
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. 游戏页面 (保留部分内部逻辑用于演示，主页使用外部链接)
# ==========================================
# 这里保留函数是为了代码完整性，实际上主页将跳转到外部链接
def render_life_stats():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.markdown("<h1 style='text-align:center; font-size:4rem; margin-bottom:10px'>Life Stats</h1>", unsafe_allow_html=True)
    # ... (省略具体实现，主页点击将跳出)

def render_spend_money():
    # ... (省略具体实现，主页点击将跳出)
    pass

def render_stack_rocks():
    # ... (省略具体实现，主页点击将跳出)
    pass

def render_deep_sea():
    # ... (省略具体实现，主页点击将跳出)
    pass

# ==========================================
# 10. 主页 (Home) - 核心展示区
# ==========================================
def render_home():
    # 右上角按钮
    render_top_right_button()
    
    # 主标题 + 副标题
    st.markdown("<h1 style='text-align:center; font-size:4rem; margin-bottom:10px;'>Neal.fun</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>A collection of silly little projects and games</p>", unsafe_allow_html=True)
    
    # 游戏配置列表 - 已更新为外部真实链接 (URL)
    games = [
        ("Life Stats", "How long have you lived?", "📅", "https://neal.fun/life-stats/"),
        ("Spend Money", "Spend Bill Gates' money", "💸", "https://neal.fun/spend/"),
        ("Stack Rocks", "A calming rock game", "🪨", "https://neal.fun/rocks/"),
        ("The Deep Sea", "Scroll to the bottom", "🌊", "https://neal.fun/deep-sea/"),
        ("Space Scale", "Universe size comparison", "🪐", "https://neal.fun/size-of-space/"),
        ("Draw Circle", "Test your drawing skills", "⭕", "https://neal.fun/perfect-circle/"),
        ("Trolley Problems", "One person or five?", "🚋", "https://neal.fun/absurd-trolley-problems/"),
        ("Password Game", "Choose a password", "🔒", "https://neal.fun/password-game/"),
        ("Street View", "Weird things on maps", "🌍", "https://neal.fun/wonders-of-street-view/"),
    ]
    
    # 3列网格布局
    cols = st.columns(3)
    
    for idx, (title, desc, icon, url) in enumerate(games):
        with cols[idx % 3]:
            # 【修改核心】
            # 1. 移除 st.button (交互层)
            # 2. 直接用 <a> 标签包裹 visual card
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit; display: block;">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-content">
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # -----------------------
    # 浇水彩蛋 (全局渲染)
    # -----------------------
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">
            Watered {st.session_state.water_count} times
        </div>
        <div class="plant-emoji">🪴</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 浇水按钮
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_spacer, col_water = st.columns([10, 1])
    with col_water:
        if st.button("💧 Water"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()
    
    # 渲染底部区域
    render_footer()

# ==========================================
# 11. 程序入口
# ==========================================
def main():
    if st.session_state.page == 'home':
        render_home()
    # 注意：由于点击卡片现在会直接跳转到外部链接，
    # 这里的 elif 分支实际上不会再被首页触发，但保留以防你需要内部调试
    elif st.session_state.page == 'life_stats':
        render_life_stats()
    elif st.session_state.page == 'spend_money':
        render_spend_money()
    elif st.session_state.page == 'stack_rocks':
        render_stack_rocks()
    elif st.session_state.page == 'deep_sea':
        render_deep_sea()
        
    # 重置动画状态
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()

if __name__ == "__main__":
    main()
