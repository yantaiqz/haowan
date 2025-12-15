import streamlit as st
import datetime
import time
import random

# ==========================================
# 1. 全局配置
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
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'money' not in st.session_state:
    st.session_state.money = 100000000000
if 'rock_count' not in st.session_state:
    st.session_state.rock_count = 0

# ==========================================
# 2. CSS 样式 (核心设计灵魂)
# ==========================================
st.markdown("""
<style>
    /* 引入字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* 全局重置 */
    .stApp {
        background-color: #f3f4f6; /* 经典的浅灰背景 */
        font-family: 'Inter', sans-serif;
    }
    
    /* 隐藏 Streamlit 自带元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* ----------------------
       首页卡片样式 
       ---------------------- */
    .card-container {
        position: relative;
        background: white;
        border-radius: 20px;
        padding: 25px;
        height: 180px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e5e7eb;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        cursor: pointer;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #d1d5db;
    }
    
    .card-icon {
        font-size: 40px;
        margin-bottom: 10px;
    }
    
    .card-title {
        font-weight: 800;
        font-size: 1.2rem;
        color: #1f2937;
        margin-bottom: 5px;
    }
    
    .card-desc {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.4;
    }

    /* 隐形按钮黑魔法 
       将 Streamlit 按钮拉伸覆盖在卡片上方，并设为透明
    */
    .stButton button {
        width: 100%;
        border: none;
        background: transparent;
    }
    
    /* 特别针对隐形按钮的类 */
    div.row-widget.stButton {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        z-index: 10; /* 确保按钮在文字上方 */
    }
    
    div.row-widget.stButton > button {
        width: 100%;
        height: 100%;
        background-color: transparent;
        color: transparent;
        border: none;
    }
    div.row-widget.stButton > button:hover {
        background-color: transparent;
        color: transparent;
        border: none;
    }
    div.row-widget.stButton > button:focus {
        box-shadow: none;
        background-color: transparent;
        color: transparent;
    }

    /* ----------------------
       普通功能按钮样式 (返回键等)
       ---------------------- */
    .nav-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-weight: 600;
        color: #333;
        text-decoration: none;
        margin-bottom: 20px;
        cursor: pointer;
    }

    /* ----------------------
       浇水彩蛋样式
       ---------------------- */
    .plant-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        text-align: center;
        z-index: 9999;
    }
    .water-bubble {
        background: white;
        padding: 5px 10px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        opacity: 0;
        transition: opacity 0.5s;
        margin-bottom: 5px;
    }
    .show-bubble { opacity: 1; }
    
    .plant-emoji { font-size: 50px; cursor: pointer; }
    
    @keyframes tilt-shaking {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(5deg); }
        50% { transform: rotate(0deg); }
        75% { transform: rotate(-5deg); }
        100% { transform: rotate(0deg); }
    }
    .shake { animation: tilt-shaking 0.3s infinite; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 辅助函数
# ==========================================
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 4. 游戏页面组件
# ==========================================

def render_life_stats():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("📅 Life Stats")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        bday = st.date_input("When were you born?", datetime.date(2000, 1, 1))
    
    now = datetime.datetime.now()
    delta = now - datetime.datetime.combine(bday, datetime.time())
    seconds = int(delta.total_seconds())
    
    st.markdown(f"""
    <div style='padding:40px; background:white; border-radius:20px; text-align:center; margin-top:20px;'>
        <div style='font-size: 20px; color:#666'>You have been alive for</div>
        <div style='font-size: 60px; font-weight:900; color:#111'>{seconds:,}</div>
        <div style='font-size: 20px; color:#666'>seconds</div>
        <br>
        <div style='display:flex; justify-content:space-around;'>
            <div>
                <div style='font-size:30px; font-weight:bold'>{delta.days:,}</div>
                <div style='color:#999'>Days</div>
            </div>
            <div>
                <div style='font-size:30px; font-weight:bold'>{int(seconds/3600):,}</div>
                <div style='color:#999'>Hours</div>
            </div>
            <div>
                <div style='font-size:30px; font-weight:bold'>{int(seconds * 1.3):,}</div>
                <div style='color:#999'>Heartbeats</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_spend_money():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    
    # 顶部悬浮条
    st.markdown(f"""
    <div style='position:fixed; top:0; left:0; width:100%; background:#2ecc71; color:white; text-align:center; padding:15px; font-size:24px; font-weight:bold; z-index:99;'>
        ${st.session_state.money:,.0f}
    </div>
    <br><br>
    """, unsafe_allow_html=True)
    
    st.title("💸 Spend Bill Gates' Money")
    
    items = [
        ("Big Mac", 2, "🍔"), ("Coffee", 5, "☕"), ("Book", 15, "📚"),
        ("Airpods", 199, "🎧"), ("Smartphone", 999, "📱"), ("Rolex", 15000, "⌚"),
        ("Tesla", 75000, "🚗"), ("House", 500000, "🏠"), ("Yacht", 7000000, "🚢"),
        ("NBA Team", 2120000000, "🏀")
    ]
    
    cols = st.columns(3)
    for i, (name, price, icon) in enumerate(items):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"<div style='font-size:40px; text-align:center'>{icon}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:bold; text-align:center'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color:#2ecc71; font-weight:bold; text-align:center'>${price:,}</div>", unsafe_allow_html=True)
                
                if st.button(f"Buy", key=f"buy_{i}", use_container_width=True, disabled=st.session_state.money < price):
                    st.session_state.money -= price
                    st.rerun()

def render_stack_rocks():
    st.button("← Back", on_click=lambda: navigate_to('home'))
    st.title("🪨 Stacking Rocks")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Add Rock", type="primary", use_container_width=True):
            st.session_state.rock_count += 1
        if st.button("Reset", use_container_width=True):
            st.session_state.rock_count = 0
            
    with col2:
        # 可视化堆叠
        rocks_visual = ""
        for i in range(st.session_state.rock_count):
            # 随机一点偏移，让石头看起来自然
            offset = random.randint(-10, 10)
            width = max(50, 200 - i*5) # 越往上越小
            rocks_visual = f"""
            <div style='width:{width}px; height:40px; background:#7f8c8d; border-radius:10px; margin:0 auto; margin-bottom:-5px; transform:translateX({offset}px); border:2px solid #555;'></div>
            """ + rocks_visual
            
        st.markdown(f"""
        <div style='height:600px; display:flex; flex-direction:column; justify-content:flex-end; padding-bottom:20px;'>
            {rocks_visual}
            <div style='text-align:center; color:#999; margin-top:20px'>Count: {st.session_state.rock_count}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. 首页渲染 (修复网格逻辑)
# ==========================================
def render_home():
    st.markdown("<h1 style='text-align:center; font-size: 60px; margin-bottom: 40px;'>Neal.fun</h1>", unsafe_allow_html=True)
    
    games = [
        ("Life Stats", "How long have you lived?", "📅", "life_stats"),
        ("Spend Money", "Spend $100b in 60s", "💸", "spend_money"),
        ("Stack Rocks", "A relaxing rock game", "🪨", "stack_rocks"),
        ("The Deep Sea", "Explore the ocean", "🌊", "home"), # 占位
        ("Space Scale", "Universe size comparison", "🪐", "home"), # 占位
        ("Draw Circle", "Test your drawing skills", "⭕", "home"), # 占位
    ]

    # 创建 3 列布局
    cols = st.columns(3)
    
    for index, (title, desc, icon, target) in enumerate(games):
        # 计算当前卡片应该在第几列
        with cols[index % 3]:
            # 这是一个相对定位的容器，用于包裹视觉层和交互层
            container_html = f"""
            <div class="card-container">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """
            st.markdown(container_html, unsafe_allow_html=True)
            
            # 隐形按钮：覆盖在上面的 markdown 上
            # 注意：Streamlit 按钮默认有 margin，CSS 中必须重置
            if st.button(" ", key=f"btn_{index}"):
                navigate_to(target)

    # --------------------------
    # 浇水彩蛋 (右下角)
    # --------------------------
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    plant_html = f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">
            Watered {st.session_state.water_count} times
        </div>
        <div class="plant-emoji">🪴</div>
    </div>
    """
    st.markdown(plant_html, unsafe_allow_html=True)
    
    # 浇水按钮 (同样使用隐形按钮技巧，定位在右下角)
    # 由于Streamlit限制，这里用 columns 来放置一个按钮，尽量靠近位置
    # 完美方案需要更复杂的CSS hack，这里使用一个简单版本：
    # 我们在页面最底部放一个不可见的按钮，通过JS或CSS挪过去
    # (为了稳定性，这里使用一个简单的侧边栏按钮或直接在下方模拟)
    
    # 简单实现：直接显示在侧边栏或者页面底部
    with st.sidebar:
         st.write("Debug: Plant Waterer")
         if st.button("Water Plant 💧"):
             st.session_state.water_count += 1
             st.session_state.trigger_water = True
             st.rerun()

# ==========================================
# 6. 程序入口
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
        
    # 浇水动画计时器重置
    if st.session_state.trigger_water:
        time.sleep(1)
        st.session_state.trigger_water = False
        st.rerun()

if __name__ == "__main__":
    main()
