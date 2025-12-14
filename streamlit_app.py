import streamlit as st
import time
import pandas as pd

# -------------------------- 全局配置 --------------------------
st.set_page_config(
    page_title="Neal.fun Clone",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入 CSS 以模仿 Neal.fun 的极简风格
st.markdown("""
<style>
    /* 隐藏默认菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 大标题风格 */
    .big-font {
        font-size: 50px !important;
        font-weight: 800;
        text-align: center;
        color: #333;
        margin-bottom: 20px;
    }
    
    /* 卡片风格 */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* 统计数字 */
    .money-counter {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #2ecc71;
        color: white;
        text-align: center;
        font-size: 30px;
        padding: 15px;
        z-index: 999;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 居中容器 */
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 游戏 1: 花光比尔盖茨的钱 --------------------------
def game_spend_money():
    # 初始总金额 (1000亿美元)
    TOTAL_MONEY = 100000000000
    
    # 商品数据
    items = [
        {"name": "巨无霸", "price": 2, "icon": "🍔"},
        {"name": "星巴克咖啡", "price": 5, "icon": "☕"},
        {"name": "AirPods", "price": 199, "icon": "🎧"},
        {"name": "游戏主机", "price": 499, "icon": "🎮"},
        {"name": "名牌包包", "price": 2000, "icon": "👜"},
        {"name": "喷气式滑雪板", "price": 12000, "icon": " jetski"}, # Emoji workaround
        {"name": "特斯拉", "price": 45000, "icon": "🚗"},
        {"name": "法拉利", "price": 250000, "icon": "🏎️"},
        {"name": "独立屋", "price": 500000, "icon": "🏠"},
        {"name": "金条", "price": 700000, "icon": "🧈"},
        {"name": "麦当劳加盟店", "price": 1500000, "icon": "🍟"},
        {"name": "超级游艇", "price": 7500000, "icon": "🚢"},
        {"name": "M1艾布拉姆斯坦克", "price": 8000000, "icon": "🚜"},
        {"name": "波音747", "price": 148000000, "icon": "✈️"},
        {"name": "蒙娜丽莎", "price": 860000000, "icon": "🖼️"},
        {"name": "摩天大楼", "price": 1000000000, "icon": "🏙️"},
        {"name": "NBA球队", "price": 3000000000, "icon": "🏀"},
    ]

    # 初始化 Session State
    if "cart" not in st.session_state:
        st.session_state.cart = {item["name"]: 0 for item in items}

    # 计算余额
    spent = sum(st.session_state.cart[item["name"]] * item["price"] for item in items)
    balance = TOTAL_MONEY - spent

    # 顶部悬浮金额条
    st.markdown(f'<div class="money-counter">余额: ${balance:,.0f}</div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True) # 占位符
    
    st.markdown('<p class="big-font">💸 花光比尔盖茨的钱</p>', unsafe_allow_html=True)
    st.write("尝试买下所有东西，体验有钱人的枯燥。")

    # 网格布局展示商品
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"<h1 style='text-align: center;'>{item['icon']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{item['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: green; font-weight: bold;'>${item['price']:,}</p>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 1, 1])
                
                # 卖出按钮
                with c1:
                    if st.button("卖出", key=f"sell_{i}", disabled=st.session_state.cart[item["name"]] == 0):
                        st.session_state.cart[item["name"]] -= 1
                        st.rerun()
                
                # 数量显示
                with c2:
                    st.markdown(f"<div style='text-align: center; line-height: 2.5;'><b>{st.session_state.cart[item['name']]}</b></div>", unsafe_allow_html=True)
                
                # 买入按钮
                with c3:
                    if st.button("买入", key=f"buy_{i}", disabled=balance < item["price"]):
                        st.session_state.cart[item["name"]] += 1
                        st.rerun()

    # 收据
    if spent > 0:
        st.divider()
        st.subheader("🧾 购物收据")
        receipt_data = []
        for item in items:
            qty = st.session_state.cart[item["name"]]
            if qty > 0:
                receipt_data.append({
                    "商品": item["name"],
                    "数量": qty,
                    "单价": f"${item['price']:,}",
                    "总计": f"${qty * item['price']:,}"
                })
        st.table(pd.DataFrame(receipt_data))

# -------------------------- 游戏 2: 荒谬电车难题 --------------------------
def game_trolley():
    st.markdown('<p class="big-font">🚃 荒谬电车难题</p>', unsafe_allow_html=True)
    
    questions = [
        {
            "q": "一辆失控的电车冲过来了。如果你拉动拉杆，电车会变道撞死 1 个人。如果你不拉，它会撞死 5 个人。",
            "img": "🚋 💨 🛤️ 🚶‍♂️🚶‍♂️🚶‍♂️🚶‍♂️🚶‍♂️ vs 🛤️ 🚶‍♂️",
            "opt1": "什么都不做 (死5人)",
            "opt2": "拉动拉杆 (死1人)",
            "stat": 85 # 假设85%的人选择拉杆
        },
        {
            "q": "电车冲过来了。轨道上有一个好朋友。另一条轨道上有五个陌生人。",
            "img": "🚋 💨 🛤️ 👯‍♂️ (朋友) vs 🛤️ 🚶‍♂️🚶‍♂️🚶‍♂️🚶‍♂️🚶‍♂️ (陌生人)",
            "opt1": "救朋友 (死5个陌生人)",
            "opt2": "救陌生人 (死1个朋友)",
            "stat": 40
        },
        {
            "q": "电车冲过来了。轨道上是你刚买的iPhone 16 Pro Max (未拆封)。另一条轨道上是一个快退休的老人。",
            "img": "🚋 💨 🛤️ 📱 vs 🛤️ 👴",
            "opt1": "救 iPhone",
            "opt2": "救老人",
            "stat": 12
        }
    ]
    
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        
    idx = st.session_state.q_index
    
    if idx < len(questions):
        q = questions[idx]
        
        st.markdown(f"<h2 style='text-align: center;'>{q['img']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{q['q']}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(q['opt1'], use_container_width=True, type="secondary"):
                st.session_state.last_choice = "opt1"
                st.session_state.show_result = True
                st.rerun()
        with col2:
            if st.button(q['opt2'], use_container_width=True, type="primary"):
                st.session_state.last_choice = "opt2"
                st.session_state.show_result = True
                st.rerun()
                
        if st.session_state.get("show_result"):
            st.info(f"📊 大数据统计：{q['stat']}% 的人同意你的选择（或是另外的选择）。")
            time.sleep(1.5)
            if st.button("下一题 ➡️"):
                st.session_state.q_index += 1
                st.session_state.show_result = False
                st.rerun()
    else:
        st.success("你完成了所有道德审判！你是一个冷酷无情的人吗？还是理性的功利主义者？")
        if st.button("重新开始"):
            st.session_state.q_index = 0
            st.rerun()

# -------------------------- 主导航逻辑 --------------------------
def main():
    st.sidebar.title("🎮 Neal.fun 复刻")
    app_mode = st.sidebar.radio("选择游戏", ["花光比尔盖茨的钱", "荒谬电车难题"])
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Made with Streamlit by You")
    
    if app_mode == "花光比尔盖茨的钱":
        game_spend_money()
    elif app_mode == "荒谬电车难题":
        game_trolley()

if __name__ == "__main__":
    main()
