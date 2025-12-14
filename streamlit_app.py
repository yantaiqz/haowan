import streamlit as st
import datetime
import time
import pandas as pd

# ==========================================
# 1. 全局配置与 CSS 魔法
# ==========================================
st.set_page_config(page_title="Neal.fun Clone", page_icon="🦕", layout="wide")

# 注入 CSS 以模仿 Neal.fun 的风格
st.markdown("""
<style>
    /* 全局字体和背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #fdfdfd;
    }

    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 标题样式 */
    h1, h2, h3 {
        font-weight: 900 !important;
        color: #1a1a1a;
    }

    /* 首页卡片样式 */
    .game-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        border: 2px solid #eee;
        cursor: pointer;
        height: 100%;
    }
    .game-card:hover {
        transform: translateY(-5px);
        border-color: #333;
    }
    .emoji-icon {
        font-size: 60px;
        margin-bottom: 10px;
    }
    
    /* 余额悬浮条 */
    .money-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #2ecc71;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        z-index: 999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* 统计数字大字体 */
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        color: #333;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 状态管理
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# 3. 模块：Life Stats (生命数据)
# ==========================================
def render_life_stats():
    st.button("← 返回首页", on_click=lambda: navigate_to('home'))
    
    st.title("📅 Life Stats")
    st.write("输入你的生日，看看宇宙为你记录了什么。")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        birthday = st.date_input("你的生日", datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1))
    
    now = datetime.datetime.now()
    birth_dt = datetime.datetime.combine(birthday, datetime.time())
    delta = now - birth_dt
    
    seconds_lived = delta.total_seconds()
    days_lived = delta.days
    
    # 简单的估算逻辑
    heartbeats = seconds_lived * 1.3  # 平均每秒1.3次
    breaths = seconds_lived * 0.25    # 平均每秒0.25次
    distance_sun = seconds_lived * 29.78 # 地球公转速度 29.78 km/s
    
    st.divider()
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"<div class='stat-number'>{int(seconds_lived):,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>你在这个星球上存活的秒数</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='stat-number'>{int(heartbeats):,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>你的心脏大约跳动的次数</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='stat-number'>{days_lived:,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>你度过的天数</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='stat-number'>{int(distance_sun):,} km</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>你随地球在太空中旅行的距离</div>", unsafe_allow_html=True)
        
    st.info("💡 提示：这只是基于平均值的估算。")

# ==========================================
# 4. 模块：Spend Bill Gates' Money (花光首富)
# ==========================================
def render_spend_money():
    # 顶部余额条
    TOTAL_ASSETS = 100000000000
    
    # 商品列表
    items = [
        {"name": "巨无霸", "price": 2, "icon": "🍔"},
        {"name": "人字拖", "price": 3, "icon": "🩴"},
        {"name": "可乐", "price": 5, "icon": "🥤"},
        {"name": "电影票", "price": 12, "icon": "🎟️"},
        {"name": "图书", "price": 15, "icon": "📚"},
        {"name": "龙虾晚餐", "price": 45, "icon": "🦞"},
        {"name": "游戏机", "price": 299, "icon": "🎮"},
        {"name": "智能手机", "price": 699, "icon": "📱"},
        {"name": "无人机", "price": 999, "icon": "🚁"},
        {"name": "名牌包", "price": 2700, "icon": "👜"},
        {"name": "热水浴缸", "price": 6000, "icon": "🛁"},
        {"name": "钻石戒指", "price": 10000, "icon": "💍"},
        {"name": "快艇", "price": 30000, "icon": "🚤"},
        {"name": "特斯拉", "price": 75000, "icon": "🚗"},
        {"name": "怪兽卡车", "price": 150000, "icon": "🚜"},
        {"name": "法拉利", "price": 250000, "icon": "🏎️"},
        {"name": "单户住宅", "price": 300000, "icon": "🏠"},
        {"name": "金条", "price": 700000, "icon": "🧈"},
        {"name": "麦当劳加盟店", "price": 1500000, "icon": "🍟"},
        {"name": "超级游艇", "price": 7500000, "icon": "🚢"},
        {"name": "M1坦克", "price": 8000000, "icon": "🛡️"},
        {"name": "F1赛车", "price": 15000000, "icon": "🏎️"},
        {"name": "波音747", "price": 148000000, "icon": "✈️"},
        {"name": "蒙娜丽莎", "price": 780000000, "icon": "🖼️"},
        {"name": "摩天大楼", "price": 850000000, "icon": "🏙️"},
        {"name": "游轮", "price": 930000000, "icon": "🛳️"},
        {"name": "NBA球队", "price": 2120000000, "icon": "🏀"},
    ]

    # 初始化购物车
    if "cart" not in st.session_state:
        st.session_state.cart = {item["name"]: 0 for item in items}

    # 计算
    spent = sum(st.session_state.cart[item["name"]] * item["price"] for item in items)
    balance = TOTAL_ASSETS - spent

    # 渲染顶部
    st.markdown(f'<div class="money-bar">余额: ${balance:,.0f}</div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True) # 占位
    
    st.button("← 没钱了，回家", on_click=lambda: navigate_to('home'))
    st.markdown("# 💸 花光比尔盖茨的钱")
    
    # 商品网格
    cols = st.columns(3)
    for index, item in enumerate(items):
        with cols[index % 3]:
            with st.container(border=True):
                st.markdown(f"<div style='text-align:center; font-size:40px'>{item['icon']}</div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align:center; margin:0'>{item['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center; color:#2ecc71; font-weight:bold'>${item['price']:,}</p>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,1])
                qty = st.session_state.cart[item["name"]]
                
                with c1:
                    if st.button("卖出", key=f"s_{index}", disabled=qty==0):
                        st.session_state.cart[item["name"]] -= 1
                        st.rerun()
                with c2:
                    st.markdown(f"<div style='text-align:center; font-weight:bold; padding-top:10px'>{qty}</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("买入", key=f"b_{index}", disabled=balance < item["price"]):
                        st.session_state.cart[item["name"]] += 1
                        st.rerun()
    
    if spent > 0:
        st.divider()
        st.markdown("### 🧾 收据")
        st.write(f"你总共挥霍了: **${spent:,.0f}**")

# ==========================================
# 5. 模块：The Deep Scroll (深渊)
# ==========================================
def render_deep_scroll():
    st.button("← 浮出水面", on_click=lambda: navigate_to('home'))
    st.title("🌊 The Deep Scroll")
    st.markdown("*持续向下滚动，探索海洋的深度... (模拟版)*")
    
    # 定义深度数据
    depths = [
        (0, "🌊 海平面", "你可以呼吸。"),
        (20, "🐠 珊瑚礁", "小丑鱼在这里生活。"),
        (40, "🤿 休闲潜水极限", "大多数游客到这里就停了。"),
        (100, "🐋 蓝鲸", "地球上最大的动物出没于此。"),
        (300, "🗼 埃菲尔铁塔", "如果把它扔进水里，塔尖在这里。"),
        (500, "🐧 帝企鹅", "它们能潜这么深，惊人吧？"),
        (828, "🏙️ 哈利法塔", "世界最高楼也淹没于此。"),
        (1000, "🦑 巨型乌贼", "这里开始进入‘午夜区’，阳光无法到达。"),
        (3800, "🚢 泰坦尼克号残骸", "这里一片漆黑，只有深潜器能到达。"),
        (10994, "🏁 马里亚纳海沟", "地球的最深处。你触底了。")
    ]
    
    # 使用 slider 模拟深度探索（因为 Streamlit 难以检测滚动事件）
    depth = st.slider("下潜深度 (米)", 0, 11000, 0, step=10)
    
    # 动态背景颜色计算 (浅蓝 -> 深黑)
    # 0m = #4facfe, 11000m = #000000
    ratio = min(depth / 5000, 1) # 5000米后就全黑
    r = int(79 * (1-ratio))
    g = int(172 * (1-ratio))
    b = int(254 * (1-ratio))
    bg_color = f"rgb({r},{g},{b})"
    
    # 强制修改背景色的容器
    st.markdown(f"""
    <div style="
        background-color: {bg_color}; 
        padding: 50px; 
        border-radius: 20px; 
        color: {'white' if depth > 300 else 'black'};
        text-align: center;
        min-height: 400px;
        transition: background-color 0.5s;
    ">
        <h1 style="color: inherit">{depth} 米</h1>
        <br>
    """, unsafe_allow_html=True)
    
    # 查找当前深度附近的生物
    closest_item = min(depths, key=lambda x: abs(x[0] - depth))
    
    if abs(closest_item[0] - depth) < 150: # 如果距离地标150米以内
        st.markdown(f"""
        <div style="background-color:rgba(255,255,255,0.2); padding:20px; border-radius:10px; display:inline-block">
            <div style="font-size: 80px">{closest_item[1].split(' ')[0]}</div>
            <h2>{closest_item[1].split(' ')[1]}</h2>
            <p>{closest_item[2]}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<br><br><i>除了海水，什么都没有...</i><br><br>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. 主页与路由
# ==========================================
def render_home():
    st.title("🦕 Neal.fun (Streamlit 复刻版)")
    st.write("一系列毫无意义但有趣的网页玩具。")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <div class="emoji-icon">📅</div>
            <h3>Life Stats</h3>
            <p>看看你在这个地球上存在了多久。</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("玩 Life Stats", use_container_width=True):
            navigate_to('life_stats')

    with col2:
        st.markdown("""
        <div class="game-card">
            <div class="emoji-icon">💸</div>
            <h3>Spend Bill Gates' Money</h3>
            <p>给你 1000 亿美元，你能在 60 秒内花完吗？</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("玩 Spend Money", use_container_width=True):
            navigate_to('spend_money')

    with col3:
        st.markdown("""
        <div class="game-card">
            <div class="emoji-icon">🌊</div>
            <h3>The Deep Sea</h3>
            <p>下潜到海洋最深处，看看那里有什么。</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("玩 The Deep", use_container_width=True):
            navigate_to('deep_scroll')
    
    st.markdown("<br><br><br><div style='text-align:center; color:#ccc'>Inspired by Neal.fun | Made with Streamlit</div>", unsafe_allow_html=True)

# ==========================================
# 7. 程序入口
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
