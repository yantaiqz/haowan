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

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'money' not in st.session_state:
    st.session_state.balance = 100000000000
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'rock_count' not in st.session_state:
    st.session_state.rock_count = 0

# ==========================================
# 2. 核心 CSS 样式 (Neal.fun Design System)
# ==========================================
st.markdown("""
<style>
    /* 引入字体 Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* 【修改点1】全局背景改为白色 */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }

    /* 隐藏无关元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        letter-spacing: -1px;
        color: #111;
    }

    /* ----------------------
       Neal.fun 卡片样式
       ---------------------- */
    .neal-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        /* 【修改点2】调整Padding和高度，使其更接近原版比例 */
        padding: 25px 20px;
        height: 175px; 
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
    }

    .neal-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #D1D5DB;
        z-index: 1;
    }

    .card-icon { font-size: 42px; margin-bottom: 12px; }
    .card-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 6px; color: #111; }
    .card-desc { font-size: 0.9rem; color: #6B7280; line-height: 1.4; }

    /* ----------------------
       隐形按钮黑魔法 (用于卡片跳转)
       ---------------------- */
    div[data-testid="column"] .stButton {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        z-index: 5; margin: 0 !important;
    }
    div[data-testid="column"] .stButton > button {
        width: 100%; height: 100%; background: transparent; color: transparent; border: none;
    }
    div[data-testid="column"] .stButton > button:hover, div[data-testid="column"] .stButton > button:focus {
        background: transparent; color: transparent; border: none; outline: none; box-shadow: none;
    }

    /* ----------------------
       【修改点4 & 5】顶部和底部特定按钮样式美化
       Targeting st.link_button to look like Neal.fun buttons
       ---------------------- */
    [data-testid="stLinkButton"] > a {
        border: 1px solid #E5E7EB !important;
        background: white !important;
        color: #111 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        transition: all 0.2s !important;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stLinkButton"] > a:hover {
         background: #f9fafb !important;
         border-color: #111 !important;
         transform: translateY(-2px);
         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* 游戏内返回按钮样式 */
    .back-btn-wrapper button {
        background: white !important; color: #333 !important; border: 1px solid #ddd !important;
    }

    /* 余额悬浮条 */
    .money-bar {
        position: fixed; top: 0; left: 0; width: 100%; background: #2ecc71; color: white;
        text-align: center; padding: 15px; font-size: 24px; font-weight: 800; z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 路由与辅助
# ==========================================
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def render_footer():
    """【修改点4】渲染底部Footer"""
    st.markdown("<br><br><hr style='margin: 40px 0; border-color: #eee;'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#666; font-weight:600; margin-bottom: 25px;'>Made with ❤️ by Neal Agarwal (Clone)</div>", unsafe_allow_html=True)
    
    # 使用列来居中排列底部的三个按钮
    # 使用空列来挤压中间的内容
    c_spacer1, c_btn1, c_btn2, c_btn3, c_spacer2 = st.columns([3, 2, 2, 2, 3])
    with c_btn1:
        st.link_button("📰 Newsletter", "https://neal.fun/newsletter/", use_container_width=True)
    with c_btn2:
        st.link_button("🐦 Twitter", "https://twitter.com/nealagarwal", use_container_width=True)
    with c_btn3:
        st.link_button("☕ Buy coffee", "https://www.buymeacoffee.com/nealagarwal", use_container_width=True)
    st.markdown("<br><br>", unsafe_allow_html=True)


# ==========================================
# 4. 游戏页面 (简化版)
# ==========================================
def render_life_stats():
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("📅 Life Stats")
    st.write("See how long you've lasted.")
    
    bday = st.date_input("Select Birthday", datetime.date(2000, 1, 1))
    seconds = int((datetime.datetime.now() - datetime.datetime.combine(bday, datetime.time())).total_seconds())
    
    st.markdown(f"""
    <div style="background:white; padding:40px; border-radius:20px; text-align:center; border:1px solid #eee; margin-top:30px;">
        <div style="font-size:1.2rem; color:#888;">You have been alive for</div>
        <div style="font-size:4rem; font-weight:900; color:#111;">{seconds:,}</div>
        <div style="font-size:1.2rem; color:#888;">seconds</div>
    </div>
    """, unsafe_allow_html=True)

def render_spend_money():
    st.markdown(f'<div class="money-bar">Balance: ${st.session_state.balance:,.0f}</div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Exit", on_click=lambda: navigate_to('home'))
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("💸 Spend Bill Gates' Money")
    
    items = [{"name": "Big Mac", "price": 2, "icon": "🍔"}, {"name": "Airpods", "price": 199, "icon": "🎧"}, 
             {"name": "Tesla", "price": 75000, "icon": "🚗"}, {"name": "Yacht", "price": 7500000, "icon": "🚢"}]

    cols = st.columns(4) # 使用4列看起来更紧凑
    for i, item in enumerate(items):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"<div style='font-size:40px;text-align:center'>{item['icon']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:bold;text-align:center'>{item['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:#2ecc71;font-weight:bold;text-align:center'>${item['price']:,}</div>", unsafe_allow_html=True)
                if st.button("Buy", key=f"buy_{i}", use_container_width=True, disabled=st.session_state.balance < item['price']):
                    st.session_state.balance -= item['price']
                    st.rerun()

def render_stack_rocks():
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🪨 Stacking Rocks")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Add Rock 🪨", use_container_width=True): st.session_state.rock_count += 1
        if st.button("Reset", use_container_width=True): st.session_state.rock_count = 0
    with col2:
        rocks_html = ""
        random.seed(42)
        for i in range(st.session_state.rock_count):
            width = max(60, 200 - (i * 6))
            offset_x = random.randint(-20, 20)
            rotate = random.randint(-5, 5)
            color = random.choice(["#95a5a6", "#7f8c8d", "#bdc3c7"])
            rocks_html = f"""<div style="width:{width}px;height:45px;background:{color};border-radius:15px 15px 10px 10px;border:2px solid #555;margin:-10px auto 0;transform:translateX({offset_x}px) rotate({rotate}deg);"></div>""" + rocks_html
        st.markdown(f"""<div style="height:500px;border-bottom:4px solid #333;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:5px;overflow:hidden;">{rocks_html}</div>""", unsafe_allow_html=True)

# ==========================================
# 5. 主页 (Home)
# ==========================================
def render_home():
    # 【修改点3 & 5】头部重构：左侧标题/副标题，右侧按钮
    col_header, col_top_btn = st.columns([3, 1])
    
    with col_header:
        st.markdown("<h1 style='font-size:4rem; margin-bottom:10px; margin-top: 20px;'>Neal.fun</h1>", unsafe_allow_html=True)
        # 【修改点3】增加副标题
        st.markdown("<p style='font-size: 1.25rem; color: #666; font-weight: 500; margin-bottom: 50px;'>Fun projects made by Neal Agarwal</p>", unsafe_allow_html=True)
        
    with col_top_btn:
        # 【修改点5】右上角按钮，使用 st.link_button 跳转外部链接
        st.markdown("<div style='text-align: right; padding-top: 40px;'>", unsafe_allow_html=True)
        st.link_button("✨ Get new posts", "https://neal.fun/newsletter/")
        st.markdown("</div>", unsafe_allow_html=True)

    
    # 游戏列表
    games = [
        ("Life Stats", "How long have you lived?", "📅", "life_stats"),
        ("Spend Money", "Spend Bill Gates' money", "💸", "spend_money"),
        ("Stack Rocks", "A calming rock game", "🪨", "stack_rocks"),
        ("The Deep Sea", "Scroll to the bottom", "🌊", "home"),
        ("Space Scale", "Universe size comparison", "🪐", "home"),
        ("Draw Circle", "Test your drawing skills", "⭕", "home"),
    ]
    
    # 渲染卡片网格
    cols = st.columns(3)
    for idx, (title, desc, icon, target) in enumerate(games):
        with cols[idx % 3]:
            # 1. 视觉层 (HTML)
            st.markdown(f"""
            <div class="neal-card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. 交互层 (隐形按钮)
            if st.button(" ", key=f"nav_btn_{idx}"):
                if target != 'home': navigate_to(target)

    # 【修改点4】渲染底部
    render_footer()

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
    elif st.session_state.page == 'stack_rocks':
        render_stack_rocks()
