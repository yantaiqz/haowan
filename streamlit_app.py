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
# 初始化语言状态（默认中文）
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # 'zh' 中文 / 'en' 英文

# ==========================================
# 2. 多语言文本配置
# ==========================================
lang_texts = {
    'zh': {
        # 页面核心文本
        'page_title': 'AI.找乐子',
        'subtitle': '无聊而有趣的AI网页小应用',
        'top_right_btn': '✨ 获得新应用',
        # 底部文本
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_btn1': '订阅新应用 📰',
        'footer_btn2': '视频号 🐦',
        'footer_btn3': '请杯咖啡 ☕',
        'footer_creator': '老祁走❤️制作',
        # 浇水彩蛋
        'water_bubble': '已浇水 {count} 次',
        # 游戏卡片文本
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
        # 页面核心文本
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'top_right_btn': '✨ Get new apps',
        # 底部文本
        'footer_title': 'About this site',
        'footer_text': 'This is a collection of silly little projects I\'ve made over the years. None of them are particularly useful, but they\'re all fun to play with.',
        'footer_btn1': 'Newsletter 📰',
        'footer_btn2': 'Twitter 🐦',
        'footer_btn3': 'Buy me a coffee ☕',
        'footer_creator': 'Made with ❤️ by LaoQi',
        # 浇水彩蛋
        'water_bubble': 'Watered {count} times',
        # 游戏卡片文本
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

# 获取当前语言的文本配置
current_text = lang_texts[st.session_state.language]

# ==========================================
# 2. 核心 CSS (优化版 + 语言切换按钮样式)
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
       1. 右上角按钮区域 (语言切换 + Get new posts)
       ---------------------- */
    .top-right-area {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        gap: 12px; /* 按钮之间的间距 */
        align-items: center;
    }
    
    .lang-switch-btn {
        font-family: 'Inter', sans-serif;
        background: #fff;
        border: 1px solid #e5e7eb;
        color: #111;
        font-weight: 600;
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .lang-switch-btn:hover {
        background: #f9fafb;
        border-color: #111;
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
        .top-right-area {
            position: static; /* 手机上不固定，流式排列 */
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 语言切换函数
# ==========================================
def switch_language():
    """切换语言（中/英）"""
    if st.session_state.language == 'zh':
        st.session_state.language = 'en'
    else:
        st.session_state.language = 'zh'
    st.rerun()  # 重新渲染页面

# ==========================================
# 4. 页面渲染逻辑
# ==========================================
def render_home():
    # 1. 渲染右上角区域（语言切换按钮 + 获得新应用按钮）
    lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
    st.markdown(f"""
    <div class="top-right-area">
        <button class="lang-switch-btn" onclick="javascript:window.location.reload()">{lang_btn_text}</button>
        <a href="https://neal.fun/newsletter/" target="_blank" class="neal-btn-link">
            <button class="neal-btn">{current_text['top_right_btn']}</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 添加语言切换按钮（实际触发逻辑）
    # 由于HTML按钮无法直接修改session_state，这里用隐藏的streamlit按钮实现
    with st.sidebar:  # 放在侧边栏隐藏区域
        if st.button("切换语言", key="lang_switch", on_click=switch_language):
            pass

    # 2. 标题区
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # 3. 游戏卡片数据 (根据当前语言加载)
    games = current_text['games']
    
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

    # 4. Footer 区域（多语言适配）
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">
            {current_text['footer_text']}
        </div>
        <div class="footer-links">
            <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none">
                <button class="neal-btn">{current_text['footer_btn1']}</button>
            </a>
            <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration:none">
                <button class="neal-btn">{current_text['footer_btn2']}</button>
            </a>
            <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration:none">
                <button class="neal-btn">{current_text['footer_btn3']}</button>
            </a>
        </div>
        <br><br>
        <div style="color: #9CA3AF; font-size: 14px;">{current_text['footer_creator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 5. 浇水彩蛋（多语言适配）
    water_bubble_text = current_text['water_bubble'].format(count=st.session_state.water_count)
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">
            {water_bubble_text}
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
