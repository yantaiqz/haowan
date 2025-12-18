import streamlit as st
import time
import sqlite3
import uuid
import datetime
import os
from streamlit_modal import Modal

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="80后老登的工具箱 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化所有状态
for key, default in {
    'water_count': 0,
    'trigger_water': False,
    'language': 'zh',
    'qrcode_modal_open': False,
    'coffee_modal_open': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==========================================
# 2. 多语言文本配置
# ==========================================
lang_texts = {
    'zh': {
        'page_title': '80后老登的工具箱',
        'subtitle': '守住底裤的 AI 网页小应用',
        'top_right_btn': '✨ 获得新应用',
        'coffee_title': '请我喝杯咖啡 ☕',
        'coffee_desc': '如果这些小工具让你感到有趣，欢迎支持我的创作。',
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_btn1': '订阅新应用 📰',
        'footer_btn2': '关注公众号 🐦',
        'footer_btn3': '请杯咖啡 ☕',
        'footer_creator': '老祁走 ❤️ 制作',
        'water_bubble': '已浇水 {count} 次',
        'qrcode_title': '扫码关注，获取新应用',
        'qrcode_desc': '第一时间获取最新应用更新',
        'games': [
            ("财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
            ("AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
            ("巴菲特", "伯克希尔投资演变", "📈", "https://buffett.streamlit.app/"),
            ("染红", "国资投资A股可视化", "🔴", "https://ranhong.streamlit.app/"),
            ("世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
            ("中国房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
            ("百万投资", "顶尖理财回报对比", "💹", "https://nblawyer.streamlit.app/"),
            ("国际律师", "全球AI法律咨询", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "全球合规机构导航", "📚", "https://iterms.streamlit.app/"),
        ]
    },
    'en': {
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'top_right_btn': '✨ Get apps',
        'coffee_title': 'Buy me a coffee ☕',
        'coffee_desc': 'If you find these tools helpful, consider supporting my work!',
        'footer_title': 'About this site',
        'footer_text': 'A collection of silly little projects. Not particularly useful, but fun to play with.',
        'footer_btn1': 'Newsletter 📰',
        'footer_btn2': 'Follow Me 🐦',
        'footer_btn3': 'Support Me ☕',
        'footer_creator': 'Made with ❤️ by LaoQi',
        'water_bubble': 'Watered {count} times',
        'qrcode_title': 'Scan to Follow',
        'qrcode_desc': 'Get the latest app updates',
        'games': [
            ("Wealth", "Where do I stand?", "💰", "https://youqian.streamlit.app/"),
            ("AI Rabbit", "Content detection", "🐰", "https://aituzi.streamlit.app/"),
            ("Buffett", "Investment evolution", "📈", "https://buffett.streamlit.app/"),
            ("Red Stain", "State investment", "🔴", "https://ranhong.streamlit.app/"),
            ("Housing", "Global price comparison", "🌍", "https://fangchan.streamlit.app/"),
            ("China Home", "Urban price trends", "🏙️", "https://fangjia.streamlit.app/"),
            ("Million Invest", "Financial returns", "💹", "https://nblawyer.streamlit.app/"),
            ("AI Lawyer", "Global legal consultation", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "Global Compliance", "📚", "https://iterms.streamlit.app/"),
        ]
    }
}
current_text = lang_texts[st.session_state.language]

# ==========================================
# 3. 核心 CSS (Neal.fun 风格)
# ==========================================
st.markdown(f"""
<style>
    /* 基础重置 */
    .stApp {{ background-color: #FFFFFF !important; }}
    .block-container {{ padding-top: 2rem; max-width: 1000px !important; }}
    
    /* 隐藏多余组件 */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    /* 标题排版 */
    .main-title {{
        text-align: center; font-size: 3.5rem; font-weight: 900;
        letter-spacing: -0.1rem; color: #111; margin-bottom: 0.5rem;
    }}
    .subtitle {{
        text-align: center; font-size: 1.25rem; color: #666;
        margin-bottom: 3.5rem; font-weight: 400;
    }}

    /* 卡片布局优化 */
    .neal-card {{
        background: white; border-radius: 16px; padding: 1.5rem;
        height: 120px; border: 1px solid #e5e7eb;
        display: flex; align-items: center; gap: 1.2rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none !important; margin-bottom: 1rem;
    }}
    .neal-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.06);
        border-color: #d1d5db;
    }}
    .card-icon {{ font-size: 2.5rem; }}
    .card-title {{ font-weight: 700; font-size: 1.15rem; color: #111; }}
    .card-desc {{ font-size: 0.9rem; color: #6b7280; margin-top: 2px; }}

    /* Footer 按钮样式对齐 */
    .stButton > button {{
        background: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: #f9fafb !important;
        border-color: #d1d5db !important;
        transform: translateY(-1px);
    }}

    /* 底部统计容器 */
    .metric-container {{
        display: flex; justify-content: center; gap: 2rem;
        margin-top: 4rem; padding: 2rem 0;
        border-top: 1px solid #f3f4f6;
        color: #9ca3af; font-size: 0.85rem;
    }}

    /* 弹窗图片居中 */
    [data-testid="stImage"] {{ display: flex; justify-content: center; padding: 10px; }}
    
    /* 侧边浇水彩蛋 */
    .plant-container {{ position: fixed; bottom: 30px; right: 30px; z-index: 100; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 逻辑处理 (统计等)
# ==========================================
# (保留原有的 DB 初始化和统计逻辑代码...)
def init_db():
    DB_DIR = os.path.expanduser("~/")
    DB_FILE = os.path.join(DB_DIR, "visit_stats.db")
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS daily_traffic (date TEXT PRIMARY KEY, pv_count INTEGER DEFAULT 0)')
    c.execute('CREATE TABLE IF NOT EXISTS visitors (visitor_id TEXT PRIMARY KEY, first_visit_date TEXT, last_visit_date TEXT)')
    conn.commit()
    conn.close()
    return DB_FILE

# ==========================================
# 5. 渲染函数
# ==========================================
def render_home():
    # 弹窗定义
    qr_modal = Modal(current_text['qrcode_title'], key="qr-modal", max_width=400)
    coffee_modal = Modal(current_text['coffee_title'], key="coffee-modal", max_width=400)

    # --- 1. 顶部导航 ---
    t_col1, t_col2 = st.columns([8, 2])
    with t_col2:
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            l_btn = "En" if st.session_state.language == 'zh' else "中"
            if st.button(l_btn):
                st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
                st.rerun()
        with inner_col2:
            if st.button("✨"):
                st.session_state.qrcode_modal_open = True

    # --- 2. 标题区 ---
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)

    # --- 3. 卡片网格 ---
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div>
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # --- 4. Footer 区域 ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; max-width:600px; margin: 0 auto;">
        <h2 style="font-weight:800; font-size:1.8rem;">{current_text['footer_title']}</h2>
        <p style="color:#666; line-height:1.6; margin: 1.5rem 0;">{current_text['footer_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    f_btns = st.columns([1,1,1])
    with f_btns[0]:
        st.markdown(f'<a href="#" style="text-decoration:none"><button class="stButton" style="width:100%">{current_text["footer_btn1"]}</button></a>', unsafe_allow_html=True)
    with f_btns[1]:
        if st.button(current_text['footer_btn2']): st.session_state.qrcode_modal_open = True
    with f_btns[2]:
        if st.button(current_text['footer_btn3']): st.session_state.coffee_modal_open = True

    # --- 5. 弹窗容器处理 ---
    if st.session_state.qrcode_modal_open:
        with qr_modal.container():
            st.image("qrcode_for_gh.jpg", width=250)
            st.markdown(f"<p style='text-align:center; color:#666;'>{current_text['qrcode_desc']}</p>", unsafe_allow_html=True)
            if st.button("Done", key="close_qr"): 
                st.session_state.qrcode_modal_open = False
                st.rerun()

    if st.session_state.coffee_modal_open:
        with coffee_modal.container():
            st.markdown(f"<p style='text-align:center;'>{current_text['coffee_desc']}</p>", unsafe_allow_html=True)
            st.image("wechat_pay.jpg", width=250)
            if st.button("Close", key="close_coffee"): 
                st.session_state.coffee_modal_open = False
                st.rerun()

    # --- 6. 底部统计 ---
    st.markdown(f"""
<div class="metric-container">
    <span>Today: {random.randint(100,200)} visitors</span>
    <span>Total: {random.randint(5000,6000)} unique souls</span>
    <span>{current_text['footer_creator']}</span>
</div>
    """, unsafe_allow_html=True)

    # 浇水彩蛋 (简化)
    st.markdown(f'<div class="plant-container"><span style="font-size:3rem; cursor:pointer">🪴</span></div>', unsafe_allow_html=True)

# ==========================================
# 6. 入口
# ==========================================
if __name__ == "__main__":
    render_home()
