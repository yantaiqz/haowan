import streamlit as st
import time
import random

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
# 初始化语言状态
if 'language' not in st.session_state:
    st.session_state.language = 'zh' 

# ==========================================
# 2. 多语言文本配置
# ==========================================
lang_texts = {
    'zh': {
        'page_title': 'AI.找乐子',
        'subtitle': '无聊而有趣的AI网页小应用',
        'top_right_btn': '✨ 获得新应用',
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_btn1': '订阅新应用 📰',
        'footer_btn2': '视频号 🐦',
        'footer_btn3': '请杯咖啡 ☕',
        'footer_creator': '老祁走❤️制作',
        'water_bubble': '已浇水 {count} 次',
        'games': [
            ("财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
            ("AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
            ("巴菲特的组合", "伯克希尔·哈撒韦投资组合演变", "📈", "https://buffett.streamlit.app/"),
            ("染红", "国资投资A股的数据可视化", "🔴", "https://ranhong.streamlit.app/"),
            ("世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
            ("城市房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
            ("百万投资", "顶尖理财产品的回报率对比", "💹", "https://nblawyer.streamlit.app/"),
            ("国际律师", "各国AI法律咨询和合同审查", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "全球法律与合规机构导航", "📚", "https://iterms.streamlit.app/"),
        ]
    },
    'en': {
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'top_right_btn': '✨ Get new apps',
        'footer_title': 'About this site',
        'footer_text': 'This is a collection of silly little projects I\'ve made over the years. None of them are particularly useful, but they\'re all fun to play with.',
        'footer_btn1': 'Newsletter 📰',
        'footer_btn2': 'Twitter 🐦',
        'footer_btn3': 'Buy me a coffee ☕',
        'footer_creator': 'Made with ❤️ by LaoQi',
        'water_bubble': 'Watered {count} times',
        'games': [
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
    }
}

current_text = lang_texts[st.session_state.language]

# ==========================================
# 3. 核心 CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }
    
    /* 调整顶部间距，给按钮留出空间 */
    .block-container { padding-top: 1rem; }
    
    /* 隐藏 Streamlit 自带元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ----------------------
       按钮样式 (统一风格)
       ---------------------- */
    /* 1. Streamlit 原生按钮 (语言切换) */
    .stButton > button {
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 6px 14px !important;
        transition: all 0.2s !important;
        height: auto !important;
        min-height: 0px !important;
        line-height: 1.5 !important;
        width: 100%; /* 填满列宽 */
    }
    .stButton > button:hover {
        background-color: #f9fafb !important;
        border-color: #111 !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* 2. HTML 链接按钮 (Get New Apps) */
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
        width: 100%;
        height: 38px; /* 强制与 st.button 高度对齐 */
    }
    .neal-btn:hover {
        background: #f9fafb;
        border-color: #111;
        transform: translateY(-1px);
    }
    .neal-btn-link { text-decoration: none; width: 100%; display: block; }

    /* 标题与卡片样式 */
    .main-title {
        text-align: center; font-size: 4rem; font-weight: 900;
        margin-bottom: 10px; margin-top: -20px; /* 因为上面有按钮列，把标题往上拉一点 */
        letter-spacing: -2px; color: #111;
    }
    .subtitle {
        text-align: center; font-size: 1.25rem; color: #6B7280;
        margin-bottom: 50px; font-weight: 400;
    }
    
    /* 卡片网格 */
    .card-link { text-decoration: none; color: inherit; display: block; margin-bottom: 20px; }
    .neal-card {
        background-color: #FFFFFF; border-radius: 16px; padding: 24px;
        height: 110px; width: 100%; border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        display: flex; flex-direction: row; align-items: center; gap: 16px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .neal-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1); border-color: #d1d5db;
    }
    .card-icon { font-size: 36px; flex-shrink: 0; }
    .card-title { font-size: 18px; font-weight: 700; margin-bottom: 4px; color: #111; }
    .card-desc { font-size: 14px; color: #6B7280; line-height: 1.4; }

    /* Footer 样式 */
    .footer-area {
        max-width: 800px; margin: 80px auto 40px; padding-top: 40px;
        border-top: 1px solid #f3f4f6; text-align: center;
        display: flex; flex-direction: column; align-items: center;
    }
    .footer-title { font-weight: 800; font-size: 1.5rem; margin-bottom: 10px; }
    .footer-text { color: #6B7280; font-size: 15px; line-height: 1.6; max-width: 500px; margin-bottom: 30px; }
    .footer-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; width: 100%; }

    /* 浇水彩蛋 */
    .plant-container { position: fixed; bottom: 20px; right: 20px; text-align: center; z-index: 999; }
    .water-bubble {
        background: white; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 700;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 6px; opacity: 0; transition: opacity 0.3s;
    }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 50px; cursor: pointer; transition: transform 0.2s; }
    .plant-emoji:hover { transform: scale(1.1); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 页面渲染逻辑
# ==========================================
def render_home():
    # ----------------------------------------------------
    # 1. 顶部按钮行 (使用 Columns 布局，稳定可靠)
    # ----------------------------------------------------
    # 布局逻辑：[ 空白占位符 (8份) ] | [ 语言按钮 (1份) ] | [ Get App 链接 (1.5份) ]
    c_spacer, c_lang, c_link = st.columns([10, 1.2, 1.8])
    
    with c_lang:
        # Streamlit 原生按钮，用于 Python 逻辑切换
        lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
        if st.button(lang_btn_text, key="lang_switch_main"):
            st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
            st.rerun()

    with c_link:
        # HTML 链接按钮
        st.markdown(f"""
        <a href="https://neal.fun/newsletter/" target="_blank" class="neal-btn-link">
            <button class="neal-btn">{current_text['top_right_btn']}</button>
        </a>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 2. 页面主体
    # ----------------------------------------------------
    # 标题区
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # 游戏卡片网格
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
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

    # Footer 区域
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">{current_text['footer_text']}</div>
        <div class="footer-links">
            <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn1']}</button></a>
            <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn2']}</button></a>
            <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn3']}</button></a>
        </div>
        <br><br>
        <div style="color: #9CA3AF; font-size: 14px;">{current_text['footer_creator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 浇水彩蛋
    water_bubble_text = current_text['water_bubble'].format(count=st.session_state.water_count)
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">{water_bubble_text}</div>
        <div class="plant-emoji">🪴</div>
    </div>
    """, unsafe_allow_html=True)

    # 隐形浇水触发器 (页面底部第二个 st.button)
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

# ==========================================
# 5. 程序入口
# ==========================================
if __name__ == "__main__":
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
