import streamlit as st
import time
import random

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="AI.找乐子",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# ==========================================
# 2. 核心 CSS (优化版)
# ==========================================
st.markdown("""
<style>
    /* 引入字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* 全局背景 */
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }
    
    /* 移除 Streamlit 顶部留白，方便放置右上角按钮 */
    .block-container {
        padding-top: 3rem;
    }

    /* 隐藏无关元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ----------------------
       1. 右上角按钮 (Get new posts)
       使用 fixed/absolute 定位，脱离文档流
       ---------------------- */
    .top-right-link {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 9999;
        text-decoration: none;
    }
    
    .neal-btn {
        font-family: 'Inter', sans-serif;
        background: #fff;
        border: 1px solid #e5e7eb;
        color: #111;
        font-weight: 600;
        font-size: 14px;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        text-decoration: none !important;
    }
    
    .neal-btn:hover {
        background: #f9fafb;
        border-color: #111;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* ----------------------
       主标题区域
       ---------------------- */
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 10px;
        letter-spacing: -2px;
        color: #111;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.25rem;
        color: #6B7280;
        margin-bottom: 50px;
        font-weight: 400;
    }

    /* ----------------------
       Neal.fun 卡片样式
       ---------------------- */
    .card-link {
        text-decoration: none;
        color: inherit;
        display: block;
        margin-bottom: 20px; /* 卡片之间的垂直间距 */
    }

    .neal-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        height: 110px;
        width: 100%;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
    }

    .neal-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
        border-color: #d1d5db;
    }

    .card-icon { font-size: 36px; flex-shrink: 0; }
    .card-title { font-size: 18px; font-weight: 700; margin-bottom: 4px; color: #111; }
    .card-desc { font-size: 14px; color: #6B7280; line-height: 1.4; }

    /* ----------------------
       3. Footer 区域 (居中 + 间距)
       ---------------------- */
    .footer-area {
        max-width: 800px;
        margin: 80px auto 40px; /* 上边距80px，水平居中 */
        padding-top: 40px;
        border-top: 1px solid #f3f4f6;
        text-align: center; /* 文本居中 */
        display: flex;
        flex-direction: column;
        align-items: center; /* Flex 子元素居中 */
    }

    .footer-title {
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    .footer-text {
        color: #6B7280;
        font-size: 15px;
        line-height: 1.6;
        max-width: 500px;
        margin-bottom: 30px;
    }

    .footer-links {
        display: flex;
        flex-wrap: wrap;       /* 允许换行 */
        justify-content: center; /* 水平居中 */
        gap: 16px;             /* 按钮之间的间距 (水平和垂直) */
        width: 100%;
    }

    /* ----------------------
       浇水彩蛋
       ---------------------- */
    .plant-container {
        position: fixed; bottom: 20px; right: 20px;
        text-align: center; z-index: 999;
    }
    .water-bubble {
        background: white; padding: 6px 10px; border-radius: 8px;
        font-size: 12px; font-weight: 700;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 6px; opacity: 0; transition: opacity 0.3s;
    }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 50px; cursor: pointer; transition: transform 0.2s; }
    .plant-emoji:hover { transform: scale(1.1); }

    /* 手机端适配 */
    @media (max-width: 768px) {
        .top-right-link {
            position: static; /* 手机上不固定，流式排列 */
            display: block;
            text-align: center;
            margin-bottom: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 页面渲染逻辑
# ==========================================

def render_home():
    # 1. 渲染右上角按钮 (直接插入 HTML)
    st.markdown("""
    <a href="https://neal.fun/newsletter/" target="_blank" class="top-right-link">
        <button class="neal-btn">✨ 获得新应用</button>
    </a>
    """, unsafe_allow_html=True)

    # 2. 标题区
    st.markdown('<div class="main-title">AI.找乐子</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">无聊而有趣的AI网页小应用</div>', unsafe_allow_html=True)
    
    # 3. 游戏卡片数据 (URL 跳转)
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
    
    # 3列布局
    cols = st.columns(3)
    
    for idx, (title, desc, icon, url) in enumerate(games):
        with cols[idx % 3]:
            # 仅渲染视觉层，外层包裹 <a> 标签实现跳转
            st.markdown(f"""
            <a href="{url}" target="_blank" class="card-link">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-content">
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # 4. Footer 区域 (完全匹配 neal.fun 的居中和按钮样式)
    st.markdown("""
    <div class="footer-area">
        <div class="footer-title">About this site</div>
        <div class="footer-text">
            This is a collection of silly little projects I've made over the years. 
            None of them are particularly useful, but they're all fun to play with.
        </div>
        <div class="footer-links">
            <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none">
                <button class="neal-btn">订阅新应用 📰</button>
            </a>
            <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration:none">
                <button class="neal-btn">视频号 🐦</button>
            </a>
            <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration:none">
                <button class="neal-btn">请杯咖啡 ☕</button>
            </a>
        </div>
        <br><br>
        <div style="color: #9CA3AF; font-size: 14px;">老祁走❤️制作</div>
    </div>
    """, unsafe_allow_html=True)

    # 5. 浇水彩蛋
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">
            Watered {st.session_state.water_count} times
        </div>
        <div class="plant-emoji">🪴</div>
    </div>
    """, unsafe_allow_html=True)

    # 隐形浇水触发器 (页面底部)
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

# ==========================================
# 4. 程序入口
# ==========================================
if __name__ == "__main__":
    render_home()
    
    # 动画计时器重置
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
