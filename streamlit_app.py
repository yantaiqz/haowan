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

# 初始化 Session State（保留浇水彩蛋状态）
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# ==========================================
# 2. 核心 CSS 样式 (保留所有视觉样式 + 超链接优化)
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
       Neal.fun 卡片样式 + 超链接优化
       ---------------------- */
    /* 卡片容器 - 适配9卡片网格 */
    .cards-container {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
        gap: 20px;
        padding: 0 10px;
    }

    /* 卡片超链接 - 核心：让整个卡片可点击 */
    .card-link {
        text-decoration: none !important;
        display: block; /* 让链接占满整个容器 */
        height: 107px; /* 匹配卡片高度 */
    }

    .neal-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px 16px;
        height: 107px; /* Neal.fun原版卡片高度 */
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: row; /* 横向布局 */
        align-items: center;
        text-align: left;
        position: relative;
        gap: 16px;
        cursor: pointer; /* 鼠标指针变为手型 */
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
        color: #111 !important; /* 超链接不改变文字颜色 */
        line-height: 1.2;
    }
    .card-desc { 
        font-size: 14px; 
        color: #6B7280 !important; /* 超链接不改变文字颜色 */
        line-height: 1.4;
    }

    /* ----------------------
       按钮样式 (保留右上角/底部按钮)
       ---------------------- */
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

    .stButton > button:hover {
        background: #F9FAFB !important;
        border-color: #D1D5DB !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
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
       功能性 CSS (保留浇水彩蛋)
       ---------------------- */
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

    /* 响应式适配 */
    @media (max-width: 1200px) {
        .cards-container {
            max-width: 900px;
        }
    }
    @media (max-width: 900px) {
        .cards-container {
            max-width: 600px;
            grid-template-columns: repeat(2, 1fr);
        }
        .top-right-btn {
            position: static;
            margin-bottom: 20px;
            text-align: right;
        }
    }
    @media (max-width: 600px) {
        .cards-container {
            max-width: 100%;
            grid-template-columns: 1fr;
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
# 3. 右上角按钮组件
# ==========================================
def render_top_right_button():
    """渲染右上角 Get New Posts 按钮"""
    st.markdown('<div class="top-right-btn">', unsafe_allow_html=True)
    st.button("Get new posts", key="top_btn", help="Subscribe to updates")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. 底部组件 (匹配neal.fun)
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
# 5. 主页 (Home) - 纯HTML卡片+外部超链接
# ==========================================
def render_home():
    # 右上角按钮
    render_top_right_button()
    
    # 主标题 + 副标题
    st.markdown("<h1 style='text-align:center; font-size:4rem; margin-bottom:10px;'>Neal.fun</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>A collection of silly little projects and games</p>", unsafe_allow_html=True)
    
    # 游戏配置列表 - 9个游戏 + 对应的外部超链接
    games = [
        ("Life Stats", "How long have you lived?", "📅", "https://neal.fun/life-stats/"),
        ("Spend Money", "Spend Bill Gates' money", "💸", "https://neal.fun/spend/"),
        ("Stack Rocks", "A calming rock game", "🪨", "https://neal.fun/stack-rocks/"),
        ("The Deep Sea", "Scroll to the bottom", "🌊", "https://neal.fun/the-deep-sea/"),
        ("Space Scale", "Explore the scale of space", "🪐", "https://neal.fun/space-scale/"),
        ("Draw Circle", "Test your circle skills", "⭕", "https://neal.fun/draw-circle/"),
        ("Color Switch", "Match colors to patterns", "🎨", "https://neal.fun/color-switch/"),
        ("Word Cloud", "Generate custom word clouds", "☁️", "https://neal.fun/word-cloud/"),
        ("Timer Game", "Simple countdown fun", "⏱️", "https://neal.fun/timer/"),
    ]
    
    # 渲染9卡片网格容器
    st.markdown('<div class="cards-container">', unsafe_allow_html=True)
    
    # 循环渲染9个带超链接的卡片（仅保留视觉层）
    for idx, (title, desc, icon, url) in enumerate(games):
        # 核心修改：用<a>标签包裹整个卡片，实现点击跳转外部网页
        card_html = f"""
        <a href="{url}" target="_blank" class="card-link">
            <div class="neal-card">
                <div class="card-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                </div>
            </div>
        </a>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    # 关闭卡片容器
    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------
    # 浇水彩蛋 (保留)
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
# 6. 程序入口
# ==========================================
def main():
    # 直接渲染主页（所有卡片都是外部链接，无需路由）
    render_home()
        
    # 重置浇水动画状态
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()

if __name__ == "__main__":
    main()
