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
       隐形按钮黑魔法
       ---------------------- */
    /* 针对卡片区域的按钮 */
    div[data-testid="column"] .stButton {
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        width: 100%; height: 100%;
        z-index: 5; /* 确保在卡片上方 */
        margin: 0 !important;
    }
    
    div[data-testid="column"] .stButton > button {
        width: 100%; height: 100%;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        background: transparent !important;
        color: transparent !important;
        border: none !important;
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
# 6. 游戏：Life Stats (生命数据)
# ==========================================
def render_life_stats():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.markdown("<h1 style='text-align:center; font-size:4rem; margin-bottom:10px'>Life Stats</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666; margin-bottom:40px'>See how long you've lasted.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        bday = st.date_input("Select your birthday", datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1))
    
    now = datetime.datetime.now()
    birth_dt = datetime.datetime.combine(bday, datetime.time())
    delta = now - birth_dt
    seconds = int(delta.total_seconds())

    # 可视化卡片
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; text-align:center; border:1px solid #eee;">
            <div style="font-size:1.2rem; color:#888; margin-bottom:10px">You have been alive for</div>
            <div style="font-size:3.5rem; font-weight:900; color:#111; line-height:1">{seconds:,}</div>
            <div style="font-size:1.2rem; color:#888; margin-top:10px">seconds</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        heartbeats = int(seconds * 1.3)
        st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; text-align:center; border:1px solid #eee;">
            <div style="font-size:1.2rem; color:#888; margin-bottom:10px">Your heart has beaten</div>
            <div style="font-size:3.5rem; font-weight:900; color:#e74c3c; line-height:1">{heartbeats:,}</div>
            <div style="font-size:1.2rem; color:#888; margin-top:10px">times</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 7. 游戏：Spend Bill Gates' Money
# ==========================================
def render_spend_money():
    # 顶部余额条
    st.markdown(f'<div class="money-bar">Balance: ${st.session_state.balance:,.0f}</div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.button("← Exit & Reset", on_click=lambda: navigate_to('home'))
    st.title("💸 Spend Bill Gates' Money")
    
    items = [
        {"name": "Big Mac", "price": 2, "icon": "🍔"},
        {"name": "Flip Flops", "price": 3, "icon": "🩴"},
        {"name": "Coca-Cola Pack", "price": 5, "icon": "🥤"},
        {"name": "Movie Ticket", "price": 12, "icon": "🎟️"},
        {"name": "Book", "price": 15, "icon": "📚"},
        {"name": "Lobster Dinner", "price": 45, "icon": "🦞"},
        {"name": "Video Game", "price": 60, "icon": "🎮"},
        {"name": "Airpods", "price": 199, "icon": "🎧"},
        {"name": "Iphone 15", "price": 999, "icon": "📱"},
        {"name": "Gaming PC", "price": 2500, "icon": "💻"},
        {"name": "Jet Ski", "price": 8000, "icon": "🚤"},
        {"name": "Rolex", "price": 15000, "icon": "⌚"},
        {"name": "Tesla Model S", "price": 75000, "icon": "🚗"},
        {"name": "Gold Bar", "price": 700000, "icon": "🧈"},
        {"name": "McDonalds Franchise", "price": 1500000, "icon": "🍟"},
        {"name": "Superbowl Ad", "price": 5250000, "icon": "📺"},
        {"name": "Yacht", "price": 7500000, "icon": "🚢"},
        {"name": "M1 Abrams", "price": 8000000, "icon": "🚜"},
        {"name": "Formula 1 Car", "price": 15000000, "icon": "🏎️"},
        {"name": "Mona Lisa", "price": 780000000, "icon": "🖼️"},
        {"name": "Skyscraper", "price": 850000000, "icon": "🏙️"},
        {"name": "NBA Team", "price": 2120000000, "icon": "🏀"},
    ]

    # 初始化购物车逻辑
    for item in items:
        if item['name'] not in st.session_state.cart:
            st.session_state.cart[item['name']] = 0

    # 3列网格展示商品
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            # 使用 Streamlit 原生容器来做边框
            with st.container(border=True):
                st.markdown(f"<div style='font-size:40px; text-align:center'>{item['icon']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:800; text-align:center; font-size:1.1rem'>{item['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:#2ecc71; font-weight:800; text-align:center'>${item['price']:,}</div>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 1, 1])
                qty = st.session_state.cart[item['name']]
                
                with c1:
                    if st.button("Sell", key=f"sell_{i}", disabled=qty==0):
                        st.session_state.cart[item['name']] -= 1
                        st.session_state.balance += item['price']
                        st.rerun()
                with c2:
                    st.markdown(f"<div style='text-align:center; padding-top:10px; font-weight:bold'>{qty}</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("Buy", key=f"buy_{i}", disabled=st.session_state.balance < item['price']):
                        st.session_state.cart[item['name']] += 1
                        st.session_state.balance -= item['price']
                        st.rerun()

# ==========================================
# 8. 游戏：Stack Rocks (叠石头)
# ==========================================
def render_stack_rocks():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("🪨 Stacking Rocks")
    st.write("Just stack them. That's it.")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Controls")
        # 主要按钮样式
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Add Rock", key="add_rock", use_container_width=True):
            st.session_state.rock_count += 1
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Reset", key="reset_rocks", type="secondary", use_container_width=True):
            st.session_state.rock_count = 0
            
    with col2:
        # 生成石头 HTML
        rocks_html = ""
        random.seed(42) # 保证每次渲染石头形状一致
        
        for i in range(st.session_state.rock_count):
            # 随机参数
            width = max(60, 200 - (i * 5))
            offset_x = random.randint(-20, 20)
            rotate = random.randint(-5, 5)
            color = random.choice(["#95a5a6", "#7f8c8d", "#bdc3c7"])
            
            rocks_html = f"""
            <div style="
                width: {width}px; 
                height: 50px; 
                background: {color}; 
                border-radius: 15px 15px 10px 10px; 
                border: 2px solid #555;
                margin: -10px auto 0; 
                transform: translateX({offset_x}px) rotate({rotate}deg);
                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            "></div>
            """ + rocks_html
            
        st.markdown(f"""
        <div style="
            height: 600px; 
            border-bottom: 5px solid #333; 
            display: flex; 
            flex-direction: column; 
            justify-content: flex-end;
            padding-bottom: 5px;
            overflow: hidden;
        ">
            {rocks_html}
            <div style="text-align:center; color:#ccc; margin-top:20px;">Count: {st.session_state.rock_count}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. 游戏：The Deep Sea (深海模拟)
# ==========================================
def render_deep_sea():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("🌊 The Deep Sea")
    
    # 用 Slider 模拟下潜
    depth = st.slider("Dive Depth (Meters)", 0, 11000, 0)
    
    # 颜色计算算法：从浅蓝 (#4facfe) 到深黑 (#000000)
    ratio = min(depth / 3000, 1) # 3000米后全黑
    r = int(79 * (1 - ratio))
    g = int(172 * (1 - ratio))
    b = int(254 * (1 - ratio))
    bg_color = f"rgb({r}, {g}, {b})"
    text_color = "black" if depth < 200 else "white"
    
    # 查找附近的物体
    milestones = [
        (0, "Surface", "Start here."),
        (20, "Coral Reef", "🐠"),
        (100, "Blue Whale", "🐋"),
        (332, "Scuba Record", "🤿"),
        (828, "Burj Khalifa", "🏙️"),
        (1000, "Midnight Zone", "🦑"),
        (3800, "Titanic", "🚢"),
        (8848, "Mt Everest (Inverted)", "🏔️"),
        (10994, "Challenger Deep", "🏁"),
    ]
    
    # 找到最近的地标
    nearest = min(milestones, key=lambda x: abs(x[0] - depth))
    message = "Just water..."
    icon = ""
    if abs(nearest[0] - depth) < 150:
        message = f"Depth: {nearest[0]}m - {nearest[1]}"
        icon = nearest[2]
        
    st.markdown(f"""
    <div class="deep-sea-box" style="background-color: {bg_color}; color: {text_color}">
        <div style="font-size: 80px;">{icon}</div>
        <h1 style="color: {text_color}">{depth} m</h1>
        <h3>{message}</h3>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. 主页 (Home) - 核心展示区
# ==========================================
def render_home():
    # 右上角按钮
    render_top_right_button()
    
    # 主标题 + 副标题
    st.markdown("<h1 style='text-align:center; font-size:4rem; margin-bottom:10px;'>Neal.fun</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>A collection of silly little projects and games</p>", unsafe_allow_html=True)
    
    # 游戏配置列表
    games = [
        ("Life Stats", "How long have you lived?", "📅", "life_stats"),
        ("Spend Money", "Spend Bill Gates' money", "💸", "spend_money"),
        ("Stack Rocks", "A calming rock game", "🪨", "stack_rocks"),
        ("The Deep Sea", "Scroll to the bottom", "🌊", "deep_sea"),
        ("Space Scale", "Coming Soon", "🪐", "home"),
        ("Draw Circle", "Coming Soon", "⭕", "home"),
    ]
    
    # 3列网格布局
    cols = st.columns(3)
    
    for idx, (title, desc, icon, target) in enumerate(games):
        with cols[idx % 3]:
            # 1. 渲染视觉层 HTML (匹配neal.fun卡片样式)
            st.markdown(f"""
            <div class="neal-card">
                <div class="card-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. 渲染交互层 Invisible Button
            if st.button(" ", key=f"nav_btn_{idx}"):
                if target != 'home':
                    navigate_to(target)

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
