import streamlit as st
import time

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"  # 保持侧边栏折叠
)

# 初始化状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # 默认中文

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
        'lang_switch_btn': '切换为英文',
        'games': [
            ("生命统计", "算算你活了多久？", "📅", "https://neal.fun/life-stats/"),
            ("花光首富的钱", "体验挥金如土的感觉", "💸", "https://neal.fun/spend/"),
            ("叠石头", "治愈系的叠石头游戏", "🪨", "https://neal.fun/rocks/"),
            ("深海探险", "一直滑到海底最深处", "🌊", "https://neal.fun/deep-sea/"),
            ("宇宙尺度", "对比宇宙万物的大小", "🪐", "https://neal.fun/size-of-space/"),
            ("画正圆", "测试你的画圆技巧", "⭕", "https://neal.fun/perfect-circle/"),
            ("电车难题", "选一个人还是五个人？", "🚋", "https://neal.fun/absurd-trolley-problems/"),
            ("密码游戏", "设置一个合规的密码", "🔒", "https://neal.fun/password-game/"),
            ("街景奇观", "地图上的神奇发现", "🌍", "https://neal.fun/wonders-of-street-view/"),
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
        'lang_switch_btn': 'Switch to Chinese',
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
# 3. 核心 CSS (优化版)
# ==========================================
st.markdown("""
<style>
    /* 全局样式 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }
    .block-container { padding-top: 3rem; }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* 右上角按钮区域 (语言切换 + 获得新应用) */
    .top-right-wrapper {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        gap: 12px;
        align-items: center;
    }

    /* 统一按钮样式 */
    .custom-btn {
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
        text-decoration: none !important;
        border: none; /* 去掉streamlit按钮默认边框 */
    }
    .custom-btn:hover {
        background: #f9fafb;
        border-color: #111;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* 标题样式 */
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

    /* 卡片样式 */
    .card-link {
        text-decoration: none;
        color: inherit;
        display: block;
        margin-bottom: 20px;
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

    /* 底部样式 */
    .footer-area {
        max-width: 800px;
        margin: 80px auto 40px;
        padding-top: 40px;
        border-top: 1px solid #f3f4f6;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
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
        flex-wrap: wrap;
        justify-content: center;
        gap: 16px;
        width: 100%;
    }

    /* 浇水彩蛋 */
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

    /* 移动端适配 */
    @media (max-width: 768px) {
        .top-right-wrapper {
            position: static;
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
    }

    /* 隐藏streamlit按钮的默认样式 */
    div[data-testid="stButton"] > button {
        all: unset; /* 清空默认样式 */
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 语言切换核心函数
# ==========================================
def switch_language():
    """切换语言并重新渲染"""
    if st.session_state.language == 'zh':
        st.session_state.language = 'en'
    else:
        st.session_state.language = 'zh'
    st.rerun()  # 关键：重新渲染页面使语言生效

# ==========================================
# 5. 页面渲染逻辑
# ==========================================
def render_home():
    # 1. 右上角区域（用streamlit按钮实现可点击的语言切换）
    st.markdown('<div class="top-right-wrapper">', unsafe_allow_html=True)
    
    # 语言切换按钮（streamlit原生按钮，绑定切换逻辑）
    lang_btn_col = st.columns([1])[0]
    with lang_btn_col:
        if st.button(
            label=current_text['lang_switch_btn'],
            key="lang_switch_btn",
            on_click=switch_language,
            use_container_width=False
        ):
            pass  # 逻辑在on_click中执行
    
    # 获得新应用按钮（HTML链接）
    st.markdown(f"""
    <a href="https://neal.fun/newsletter/" target="_blank" class="custom-btn">
        {current_text['top_right_btn']}
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. 标题区
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # 3. 游戏卡片
    games = current_text['games']
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(games):
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

    # 4. 底部区域
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">{current_text['footer_text']}</div>
        <div class="footer-links">
            <a href="https://neal.fun/newsletter/" target="_blank" class="custom-btn">{current_text['footer_btn1']}</a>
            <a href="https://twitter.com/nealagarwal" target="_blank" class="custom-btn">{current_text['footer_btn2']}</a>
            <a href="https://buymeacoffee.com/nealagarwal" target="_blank" class="custom-btn">{current_text['footer_btn3']}</a>
        </div>
        <br><br>
        <div style="color: #9CA3AF; font-size: 14px;">{current_text['footer_creator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 5. 浇水彩蛋
    water_bubble_text = current_text['water_bubble'].format(count=st.session_state.water_count)
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">{water_bubble_text}</div>
        <div class="plant-emoji">🪴</div>
    </div>
    """, unsafe_allow_html=True)

    # 浇水按钮
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

# ==========================================
# 6. 程序入口
# ==========================================
if __name__ == "__main__":
    render_home()
    
    # 重置浇水动画
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
