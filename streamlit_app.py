import streamlit as st
import time
import json
import os
from datetime import datetime

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 点击次数记录系统
# ==========================================
# 点击记录文件路径
CLICK_LOG_FILE = "app_click_stats.json"

# 初始化点击统计状态
if 'click_stats' not in st.session_state:
    # 默认统计结构
    default_stats = {
        "language_switch": 0,
        "get_new_apps": 0,
        "water_plant": 0,
        "newsletter": 0,
        "twitter": 0,
        "buy_coffee": 0,
        "apps": {},  # 存储每个应用的点击次数
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 从文件加载历史记录（如果存在）
    if os.path.exists(CLICK_LOG_FILE):
        try:
            with open(CLICK_LOG_FILE, 'r', encoding='utf-8') as f:
                st.session_state.click_stats = json.load(f)
        except:
            st.session_state.click_stats = default_stats
    else:
        st.session_state.click_stats = default_stats

# 初始化其他状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 保存点击统计到文件
def save_click_stats():
    try:
        st.session_state.click_stats["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CLICK_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.click_stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存点击统计失败: {e}")

# 记录点击次数
def record_click(click_type, app_name=None):
    """
    记录点击次数
    :param click_type: 点击类型 (language_switch, get_new_apps, water_plant, newsletter, twitter, buy_coffee, app)
    :param app_name: 应用名称（仅app类型需要）
    """
    if click_type == "app" and app_name:
        if app_name not in st.session_state.click_stats["apps"]:
            st.session_state.click_stats["apps"][app_name] = 0
        st.session_state.click_stats["apps"][app_name] += 1
    elif click_type in st.session_state.click_stats:
        st.session_state.click_stats[click_type] += 1
    
    # 保存到文件
    save_click_stats()

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
        'click_count': '点击',
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
        'click_count': 'Clicks',
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
# 3. 核心 CSS (现代字体 + 点击次数样式)
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
        --color-blue-500: #3b82f6;
        --color-green-500: #22c55e;
        --color-purple-500: #8b5cf6;
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
        position: relative;
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
        position: relative;
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

    /* 点击次数角标样式 */
    .click-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background-color: var(--color-blue-500);
        color: white !important;
        font-size: 10px !important;
        font-weight: var(--font-bold) !important;
        padding: 2px 6px;
        border-radius: 10px;
        min-width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        z-index: 10;
    }
    
    .card-click-badge {
        position: absolute;
        top: 12px;
        right: 12px;
        background-color: var(--color-green-500);
        color: white !important;
        font-size: 10px !important;
        font-weight: var(--font-bold) !important;
        padding: 2px 6px;
        border-radius: 8px;
        min-width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .plant-click-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background-color: var(--color-purple-500);
        color: white !important;
        font-size: 10px !important;
        font-weight: var(--font-bold) !important;
        padding: 2px 6px;
        border-radius: 10px;
        min-width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
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
        position: relative;
    }
    .neal-card {
        background-color: white; 
        border-radius: 12px; /* 更圆润的边角 */
        padding: 20px;
        height: 100px; 
        width: 100%; 
        border: 1px solid var(--color-gray-200);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); /* 更轻微的阴影 */
        display: flex; 
        flex-direction: row; 
        align-items: center; 
        gap: 16px;
        transition: all 0.2s ease;
        position: relative;
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
    .footer-button-wrapper {
        position: relative;
        width: 100%;
        max-width: 180px;
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
        position: relative;
    }
    .plant-emoji:hover { transform: scale(1.08); }
    
    /* 顶部按钮容器 */
    .top-btn-wrapper {
        position: relative;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 页面渲染逻辑
# ==========================================
def render_home():
    # ----------------------------------------------------
    # 1. 顶部按钮行
    # ----------------------------------------------------
    c_spacer, c_lang, c_link = st.columns([10, 1.2, 1.8])
    
    with c_lang:
        # 语言切换按钮（带点击次数标记）
        lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
        lang_clicks = st.session_state.click_stats["language_switch"]
        click_badge = f'<span class="click-badge">{lang_clicks}</span>' if lang_clicks > 0 else ""
        
        st.markdown(f"""
        <div class="top-btn-wrapper">
            <button onclick="document.getElementById('lang_switch_btn').click()" class="neal-btn">
                {lang_btn_text}
            </button>
            {click_badge}
        </div>
        """, unsafe_allow_html=True)
        
        # 隐藏的实际按钮
        if st.button(lang_btn_text, key="lang_switch_btn", visible=False):
            record_click("language_switch")
            st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
            st.rerun()

    with c_link:
        # 右上角链接按钮（带点击次数标记）
        new_app_clicks = st.session_state.click_stats["get_new_apps"]
        click_badge = f'<span class="click-badge">{new_app_clicks}</span>' if new_app_clicks > 0 else ""
        
        st.markdown(f"""
        <div class="top-btn-wrapper">
            <a href="https://neal.fun/newsletter/" target="_blank" class="neal-btn-link" onclick="recordExternalClick('get_new_apps')">
                <button class="neal-btn">{current_text['top_right_btn']}</button>
            </a>
            {click_badge}
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 2. 页面主体
    # ----------------------------------------------------
    # 标题区
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # 游戏卡片网格（带点击次数标记）
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            # 获取该应用的点击次数
            app_clicks = st.session_state.click_stats["apps"].get(title, 0)
            click_badge = f'<span class="card-click-badge">{app_clicks}</span>' if app_clicks > 0 else ""
            
            # 卡片链接（带点击记录）
            st.markdown(f"""
            <div class="card-link" onclick="recordAppClick('{title}')">
                <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="neal-card">
                        <div class="card-icon">{icon}</div>
                        <div class="card-content">
                            <div class="card-title">{title}</div>
                            <div class="card-desc">{desc}</div>
                        </div>
                        {click_badge}
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            # 隐藏按钮用于记录点击
            if st.button(f"app_click_{title}", key=f"app_btn_{idx}", visible=False):
                record_click("app", title)
                # 在新标签页打开链接
                js = f"window.open('{url}', '_blank')"
                st.components.v1.html(f"<script>{js}</script>", height=0)

    # Footer 区域
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">{current_text['footer_text']}</div>
        <div class="footer-links">
            <!-- 订阅按钮 -->
            <div class="footer-button-wrapper">
                <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none" onclick="recordExternalClick('newsletter')">
                    <button class="neal-btn">{current_text['footer_btn1']}</button>
                </a>
                {f'<span class="click-badge">{st.session_state.click_stats["newsletter"]}</span>' if st.session_state.click_stats["newsletter"] > 0 else ""}
            </div>
            
            <!-- 视频号/Twitter按钮 -->
            <div class="footer-button-wrapper">
                <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration:none" onclick="recordExternalClick('twitter')">
                    <button class="neal-btn">{current_text['footer_btn2']}</button>
                </a>
                {f'<span class="click-badge">{st.session_state.click_stats["twitter"]}</span>' if st.session_state.click_stats["twitter"] > 0 else ""}
            </div>
            
            <!-- 请咖啡按钮 -->
            <div class="footer-button-wrapper">
                <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration:none" onclick="recordExternalClick('buy_coffee')">
                    <button class="neal-btn">{current_text['footer_btn3']}</button>
                </a>
                {f'<span class="click-badge">{st.session_state.click_stats["buy_coffee"]}</span>' if st.session_state.click_stats["buy_coffee"] > 0 else ""}
            </div>
        </div>
        <div class="footer-creator">{current_text['footer_creator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 浇水彩蛋（带点击次数标记）
    water_bubble_text = current_text['water_bubble'].format(count=st.session_state.water_count)
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    water_clicks = st.session_state.click_stats["water_plant"]
    water_badge = f'<span class="plant-click-badge">{water_clicks}</span>' if water_clicks > 0 else ""
    
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">{water_bubble_text}</div>
        <div class="plant-emoji" onclick="document.getElementById('water_btn').click()">
            🪴{water_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 隐形浇水触发器
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧", key="water_btn", visible=False):
            record_click("water_plant")
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

    # JavaScript 辅助记录外部链接点击
    st.markdown("""
    <script>
    // 记录外部链接点击
    function recordExternalClick(btnType) {
        // 找到对应的隐藏按钮并点击
        const btnId = `ext_btn_${btnType}`;
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.click();
        }
    }
    
    // 记录应用点击
    function recordAppClick(appName) {
        // 找到对应的应用按钮并点击
        for (let i = 0; i < 20; i++) {
            const btn = document.getElementById(`app_btn_${i}`);
            if (btn && btn.innerText.includes(appName)) {
                btn.click();
                break;
            }
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    # 为外部链接创建隐藏按钮
    for btn_type in ["newsletter", "twitter", "buy_coffee", "get_new_apps"]:
        if st.button(f"ext_{btn_type}", key=f"ext_btn_{btn_type}", visible=False):
            record_click(btn_type)

# ==========================================
# 5. 程序入口
# ==========================================
if __name__ == "__main__":
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
        
    # 确保数据保存
    save_click_stats()
