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

# 初始化每个游戏按钮的点击计数
game_ids = [
    "wealth_rankings", "ai_rabbit", "buffett_portfolio",
    "red_stain", "global_housing", "china_housing",
    "million_investment", "international_lawyer", "legal1000"
]

# 为每个游戏ID初始化点击计数
for game_id in game_ids:
    if f'click_count_{game_id}' not in st.session_state:
        st.session_state[f'click_count_{game_id}'] = 0

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
        'click_count_text': '访问次数: {count}',
        'games': [
            ("财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
            ("AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
            ("巴菲特的组合", "伯克希尔·哈撒韦投资组合演变", "📈", "https://buffett.streamlit.app/"),
            ("染红", "国资投资A股的数据可视化", "🔴", "https://ranhong.streamlit.app/"),
            ("世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
            ("中国房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
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
        'click_count_text': 'Visits: {count}',
        'games': [
            ("Wealth Rankings", "Where do I stand?", "💰", "https://youqian.streamlit.app/"),
            ("AI Rabbit", "One-click AI content detection", "🐰", "https://aituzi.streamlit.app/"),
            ("Buffett's Portfolio", "Evolution of Berkshire Hathaway's investments", "📈", "https://buffett.streamlit.app/"),
            ("Red Stain", "Data visualization of state-owned investments in A-shares", "🔴", "https://ranhong.streamlit.app/"),
            ("Global Housing Prices", "Comparison of world city housing prices", "🌍", "https://fangchan.streamlit.app/"),
            ("China Housing Market", "Urban housing price trends", "🏙️", "https://fangjia.streamlit.app/"),
            ("Million-Dollar Investment", "Return comparison of top financial products", "💹", "https://nblawyer.streamlit.app/"),
            ("International Lawyer", "AI legal consultation & contract review worldwide", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "Global legal & compliance institution navigator", "📚", "https://iterms.streamlit.app/"),
        ]
    }
}

current_text = lang_texts[st.session_state.language]

# ==========================================
# 3. 核心 CSS (现代字体优化版)
# ==========================================
st.markdown("""
<style>
    /* 现代无衬线字体组合 - 优先使用系统原生字体保证性能 */
    :root {
        --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        --font-mono: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        
        /* 字体大小变量 */
        --text-xs: 0.75rem;    /* 12px */
        --text-sm: 0.875rem;   /* 14px */
        --text-base: 1rem;     /* 16px */
        --text-lg: 1.125rem;   /* 18px */
        --text-xl: 1.25rem;    /* 20px */
        --text-2xl: 1.5rem;    /* 24px */
        --text-3xl: 1.875rem;  /* 30px */
        --text-4xl: 2.25rem;   /* 36px */
        --text-5xl: 3rem;      /* 48px */
        
        /* 字重定义 */
        --font-light: 300;
        --font-regular: 400;
        --font-medium: 500;
        --font-semibold: 600;
        --font-bold: 700;
        --font-extrabold: 800;
        --font-black: 900;
        
        /* 颜色变量 */
        --color-gray-50: #f9fafb;
        --color-gray-100: #f3f4f6;
        --color-gray-200: #e5e7eb;
        --color-gray-300: #d1d5db;
        --color-gray-400: #9ca3af;
        --color-gray-500: #6b7280;
        --color-gray-600: #4b5563;
        --color-gray-700: #374151;
        --color-gray-800: #1f2937;
        --color-gray-900: #111827;
    }

    /* 全局字体重置 */
    * {
        font-family: var(--font-sans) !important;
        letter-spacing: -0.02em !important; /* 轻微收紧字间距，更现代 */
    }

    .stApp {
        background-color: #FFFFFF !important;
        color: var(--color-gray-900);
        line-height: 1.5; /* 统一行高 */
    }
    
    /* 调整顶部间距 */
    .block-container { 
        padding-top: 1rem; 
        max-width: 1200px !important; /* 限制最大宽度，提升阅读体验 */
    }
    
    /* 隐藏 Streamlit 自带元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ----------------------
       按钮样式 (现代简洁风格)
       ---------------------- */
    /* 1. Streamlit 原生按钮 (语言切换) */
    .stButton > button {
        background-color: white !important;
        color: var(--color-gray-800) !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: 8px !important;
        font-weight: var(--font-semibold) !important;
        font-size: var(--text-sm) !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
        height: auto !important;
        min-height: 0px !important;
        line-height: 1.5 !important;
        width: 100%;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background-color: var(--color-gray-50) !important;
        border-color: var(--color-gray-300) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }

    /* 2. HTML 链接按钮 */
    .neal-btn {
        background: white;
        border: 1px solid var(--color-gray-200);
        color: var(--color-gray-800);
        font-weight: var(--font-semibold);
        font-size: var(--text-sm);
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        text-decoration: none !important;
        width: 100%;
        height: 38px;
        box-shadow: none;
    }
    .neal-btn:hover {
        background: var(--color-gray-50);
        border-color: var(--color-gray-300);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .neal-btn-link { 
        text-decoration: none; 
        width: 100%; 
        display: block; 
    }

    /* 标题样式 - 现代层次感 */
    .main-title {
        text-align: center; 
        font-size: var(--text-5xl); 
        font-weight: var(--font-black);
        margin-bottom: 8px; 
        margin-top: -20px;
        letter-spacing: -0.05em !important; /* 标题字间距更紧凑 */
        color: var(--color-gray-900);
        line-height: 1.1; /* 标题行高更紧凑 */
    }
    .subtitle {
        text-align: center; 
        font-size: var(--text-lg); 
        color: var(--color-gray-500);
        margin-bottom: 40px; 
        font-weight: var(--font-regular);
        line-height: 1.4;
    }
    
    /* 卡片样式 - 现代简洁 */
    .card-link { 
        text-decoration: none; 
        color: inherit; 
        display: block; 
        margin-bottom: 16px; /* 减少卡片间距 */
    }
    .neal-card {
        background-color: white; 
        border-radius: 12px; /* 更圆润的边角 */
        padding: 20px;
        height: 120px; /* 增加高度以容纳点击次数 */
        width: 100%; 
        border: 1px solid var(--color-gray-200);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); /* 更轻微的阴影 */
        display: flex; 
        flex-direction: row; 
        align-items: center; 
        gap: 16px;
        transition: all 0.2s ease;
    }
    .neal-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); 
        border-color: var(--color-gray-300);
    }
    .card-icon { 
        font-size: 32px; 
        flex-shrink: 0; 
    }
    .card-title { 
        font-size: var(--text-lg); 
        font-weight: var(--font-bold); 
        margin-bottom: 2px; 
        color: var(--color-gray-900);
        line-height: 1.2;
    }
    .card-desc { 
        font-size: var(--text-sm); 
        color: var(--color-gray-500); 
        line-height: 1.3;
    }
    .card-click-count {
        font-size: var(--text-xs);
        color: var(--color-gray-400);
        margin-top: 4px;
        font-weight: var(--font-medium);
    }

    /* Footer 样式 - 现代简洁 */
    .footer-area {
        max-width: 700px; 
        margin: 60px auto 40px; 
        padding-top: 32px;
        border-top: 1px solid var(--color-gray-100); 
        text-align: center;
        display: flex; 
        flex-direction: column; 
        align-items: center;
    }
    .footer-title { 
        font-weight: var(--font-extrabold); 
        font-size: var(--text-2xl); 
        margin-bottom: 8px; 
        color: var(--color-gray-800);
    }
    .footer-text { 
        color: var(--color-gray-500); 
        font-size: var(--text-base); 
        line-height: 1.6; 
        max-width: 500px; 
        margin-bottom: 24px; 
    }
    .footer-links { 
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center; 
        gap: 12px; 
        width: 100%; 
    }
    .footer-creator {
        color: var(--color-gray-400); 
        font-size: var(--text-sm);
        margin-top: 16px;
    }

    /* 浇水彩蛋 */
    .plant-container { 
        position: fixed; 
        bottom: 20px; 
        right: 20px; 
        text-align: center; 
        z-index: 999; 
    }
    .water-bubble {
        background: white; 
        padding: 6px 10px; 
        border-radius: 8px; 
        font-size: var(--text-xs); 
        font-weight: var(--font-semibold);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
        margin-bottom: 6px; 
        opacity: 0; 
        transition: opacity 0.3s;
        color: var(--color-gray-700);
    }
    .show-bubble { opacity: 1; }
    .plant-emoji { 
        font-size: 48px; 
        cursor: pointer; 
        transition: transform 0.2s ease; 
    }
    .plant-emoji:hover { transform: scale(1.08); }
    
    /* 隐藏的点击计数按钮 */
    .click-counter-btn {
        opacity: 0;
        height: 0;
        width: 0;
        padding: 0;
        margin: 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 点击计数处理函数
# ==========================================
def increment_click_count(game_id):
    """增加指定游戏的点击计数"""
    st.session_state[f'click_count_{game_id}'] += 1
    st.rerun()

# ==========================================
# 5. 页面渲染逻辑
# ==========================================
def render_home():
    # ----------------------------------------------------
    # 1. 顶部按钮行
    # ----------------------------------------------------
    c_spacer, c_lang, c_link = st.columns([10, 1.2, 1.8])
    
    with c_lang:
        # 语言切换按钮
        lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
        if st.button(lang_btn_text, key="lang_switch_main"):
            st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
            st.rerun()

    with c_link:
        # 右上角链接按钮
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
        game_id = game_ids[idx]
        click_count = st.session_state[f'click_count_{game_id}']
        
        with cols[idx % 3]:
            # 隐藏的点击计数按钮（用于记录点击）
            click_btn_key = f"click_btn_{game_id}"
            if st.button("Click", key=click_btn_key, class_="click-counter-btn"):
                increment_click_count(game_id)
            
            # 显示游戏卡片，点击时先触发计数按钮，再跳转
            click_count_text = current_text['click_count_text'].format(count=click_count)
            st.markdown(f"""
            <a href="javascript:void(0);" onclick="document.querySelector('[data-testid=\"stButton\"] button[kind=\"secondary\"][aria-label=\"{click_btn_key}\"]').click(); setTimeout(() => window.open('{url}', '_blank'), 100);" class="card-link">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-content">
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                        <div class="card-click-count">{click_count_text}</div>
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
        <div class="footer-creator">{current_text['footer_creator']}</div>
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

    # 隐形浇水触发器
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
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
