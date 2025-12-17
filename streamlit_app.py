import streamlit as st
import time
import random
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
# 点击次数记录功能
# ==========================================
# 点击记录文件路径
CLICK_LOG_FILE = "click_stats.json"

# 初始化点击统计状态
if 'click_stats' not in st.session_state:
    st.session_state.click_stats = {
        "language_switch": 0,
        "get_new_apps": 0,
        "water_plant": 0,
        "newsletter": 0,
        "twitter": 0,
        "buy_coffee": 0,
        "game_cards": {}  # 存储每个游戏卡片的点击次数
    }
    
    # 从文件加载历史记录（如果存在）
    if os.path.exists(CLICK_LOG_FILE):
        try:
            with open(CLICK_LOG_FILE, 'r', encoding='utf-8') as f:
                saved_stats = json.load(f)
                st.session_state.click_stats.update(saved_stats)
        except:
            pass

# 初始化其他状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 保存点击统计到文件的函数
def save_click_stats():
    try:
        # 添加时间戳
        stats_to_save = st.session_state.click_stats.copy()
        stats_to_save["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CLICK_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats_to_save, f, ensure_ascii=False, indent=2)
    except:
        # 保存失败不影响主功能
        pass

# 记录点击的函数
def record_click(button_type, card_name=None):
    """
    记录按钮点击
    :param button_type: 按钮类型 (language_switch, get_new_apps, water_plant, newsletter, twitter, buy_coffee, game_card)
    :param card_name: 游戏卡片名称（仅game_card类型需要）
    """
    if button_type == "game_card" and card_name:
        if card_name not in st.session_state.click_stats["game_cards"]:
            st.session_state.click_stats["game_cards"][card_name] = 0
        st.session_state.click_stats["game_cards"][card_name] += 1
    elif button_type in st.session_state.click_stats:
        st.session_state.click_stats[button_type] += 1
    
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
        'click_count_label': '点击次数:',
        'total_clicks': '总点击数:',
        'admin_stats': '点击统计',
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
        'click_count_label': 'Clicks:',
        'total_clicks': 'Total clicks:',
        'admin_stats': 'Click Statistics',
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
# 3. 核心 CSS (现代字体优化版 + 点击次数样式)
# ==========================================
st.markdown("""
<style>
    /* 现代无衬线字体组合 */
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
    }

    /* 全局字体重置 */
    * {
        font-family: var(--font-sans) !important;
        letter-spacing: -0.02em !important;
    }

    .stApp {
        background-color: #FFFFFF !important;
        color: var(--color-gray-900);
        line-height: 1.5;
    }
    
    .block-container { 
        padding-top: 1rem; 
        max-width: 1200px !important;
    }
    
    /* 隐藏 Streamlit 自带元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* 按钮样式 */
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

    /* HTML 链接按钮 */
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

    /* 点击次数标记样式 */
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

    /* 标题样式 */
    .main-title {
        text-align: center; 
        font-size: var(--text-5xl); 
        font-weight: var(--font-black);
        margin-bottom: 8px; 
        margin-top: -20px;
        letter-spacing: -0.05em !important;
        color: var(--color-gray-900);
        line-height: 1.1;
    }
    .subtitle {
        text-align: center; 
        font-size: var(--text-lg); 
        color: var(--color-gray-500);
        margin-bottom: 40px; 
        font-weight: var(--font-regular);
        line-height: 1.4;
    }
    
    /* 卡片样式 */
    .card-link { 
        text-decoration: none; 
        color: inherit; 
        display: block; 
        margin-bottom: 16px;
        position: relative;
    }
    .neal-card {
        background-color: white; 
        border-radius: 12px;
        padding: 20px;
        height: 100px; 
        width: 100%; 
        border: 1px solid var(--color-gray-200);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
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

    /* Footer 样式 */
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
        position: relative;
    }
    .plant-emoji:hover { transform: scale(1.08); }
    
    /* 点击统计面板 */
    .stats-panel {
        position: fixed;
        top: 20px;
        left: 20px;
        background: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid var(--color-gray-200);
        z-index: 998;
        font-size: var(--text-xs);
        color: var(--color-gray-600);
        max-width: 200px;
    }
    .stats-title {
        font-weight: var(--font-bold);
        font-size: var(--text-sm);
        margin-bottom: 8px;
        color: var(--color-gray-800);
    }
    .stats-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .stats-total {
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--color-gray-100);
        font-weight: var(--font-semibold);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 页面渲染逻辑
# ==========================================
def render_home():
    # 计算总点击数
    total_clicks = (
        st.session_state.click_stats["language_switch"] +
        st.session_state.click_stats["get_new_apps"] +
        st.session_state.click_stats["water_plant"] +
        st.session_state.click_stats["newsletter"] +
        st.session_state.click_stats["twitter"] +
        st.session_state.click_stats["buy_coffee"] +
        sum(st.session_state.click_stats["game_cards"].values())
    )
    
    # 显示点击统计面板（管理员视角）
    st.markdown(f"""
    <div class="stats-panel">
        <div class="stats-title">{current_text['admin_stats']}</div>
        <div class="stats-item">
            <span>语言切换:</span>
            <span>{st.session_state.click_stats['language_switch']}</span>
        </div>
        <div class="stats-item">
            <span>获取新应用:</span>
            <span>{st.session_state.click_stats['get_new_apps']}</span>
        </div>
        <div class="stats-item">
            <span>浇水:</span>
            <span>{st.session_state.click_stats['water_plant']}</span>
        </div>
        <div class="stats-item">
            <span>游戏卡片:</span>
            <span>{sum(st.session_state.click_stats['game_cards'].values())}</span>
        </div>
        <div class="stats-total">
            <span>{current_text['total_clicks']}</span>
            <span>{total_clicks}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ----------------------------------------------------
    # 1. 顶部按钮行
    # ----------------------------------------------------
    c_spacer, c_lang, c_link = st.columns([10, 1.2, 1.8])
    
    with c_lang:
        # 语言切换按钮（带点击次数标记）
        lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
        click_badge = f'<span class="click-badge">{st.session_state.click_stats["language_switch"]}</span>' if st.session_state.click_stats["language_switch"] > 0 else ""
        
        # 自定义按钮HTML（包含点击次数标记）
        st.markdown(f"""
        <div style="position: relative;">
            <button onclick="parent.document.getElementById('lang_switch_main').click()" class="neal-btn">
                {lang_btn_text}
            </button>
            {click_badge}
        </div>
        """, unsafe_allow_html=True)
        
        # 隐藏的实际按钮（用于触发逻辑）
        if st.button(lang_btn_text, key="lang_switch_main", visible=False):
            record_click("language_switch")
            st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
            st.rerun()

    with c_link:
        # 获取新应用按钮（带点击次数标记）
        click_badge = f'<span class="click-badge">{st.session_state.click_stats["get_new_apps"]}</span>' if st.session_state.click_stats["get_new_apps"] > 0 else ""
        
        st.markdown(f"""
        <div style="position: relative;">
            <a href="https://neal.fun/newsletter/" target="_blank" class="neal-btn-link" onclick="window.parent.recordExternalClick('get_new_apps')">
                <button class="neal-btn">{current_text['top_right_btn']}</button>
            </a>
            {click_badge}
        </div>
        """, unsafe_allow_html=True)
        
        # 记录外部链接点击（通过JS）
        st.markdown("""
        <script>
        window.recordExternalClick = function(buttonType) {
            // 通过Streamlit的组件通信记录点击
            fetch('/_stcore/health', {method: 'POST'})
            .then(() => {
                // 这里通过隐藏的文本输入框传递点击事件
                const input = document.createElement('input');
                input.type = 'hidden';
                input.id = 'external_click_' + buttonType;
                input.value = Date.now();
                document.body.appendChild(input);
            });
        }
        
        // 检查并记录外部点击
        if (window.location.hash.includes('external_click')) {
            const btnType = window.location.hash.split('=')[1];
            window.recordExternalClick(btnType);
        }
        </script>
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
            # 获取该卡片的点击次数
            card_clicks = st.session_state.click_stats["game_cards"].get(title, 0)
            click_badge = f'<span class="card-click-badge">{card_clicks}</span>' if card_clicks > 0 else ""
            
            # 卡片链接（带点击次数标记）
            st.markdown(f"""
            <div class="card-link" onclick="window.parent.recordExternalClick('game_card_{title}')">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-content">
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                    {click_badge}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 记录卡片点击（使用隐藏按钮）
            if st.button(f"card_click_{title}", key=f"card_{idx}", visible=False):
                record_click("game_card", title)
                # 在新标签页打开链接
                js = f"window.open('{url}', '_blank')"
                st.components.v1.html(f"<script>{js}</script>", height=0)

    # Footer 区域
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">{current_text['footer_text']}</div>
        <div class="footer-links">
            <!-- Newsletter 按钮 -->
            <div style="position: relative; width: 100%; max-width: 180px;">
                <a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none" onclick="window.parent.recordExternalClick('newsletter')">
                    <button class="neal-btn">{current_text['footer_btn1']}</button>
                </a>
                {f'<span class="click-badge">{st.session_state.click_stats["newsletter"]}</span>' if st.session_state.click_stats["newsletter"] > 0 else ""}
            </div>
            
            <!-- Twitter 按钮 -->
            <div style="position: relative; width: 100%; max-width: 180px;">
                <a href="https://twitter.com/nealagarwal" target="_blank" style="text-decoration:none" onclick="window.parent.recordExternalClick('twitter')">
                    <button class="neal-btn">{current_text['footer_btn2']}</button>
                </a>
                {f'<span class="click-badge">{st.session_state.click_stats["twitter"]}</span>' if st.session_state.click_stats["twitter"] > 0 else ""}
            </div>
            
            <!-- Buy me a coffee 按钮 -->
            <div style="position: relative; width: 100%; max-width: 180px;">
                <a href="https://buymeacoffee.com/nealagarwal" target="_blank" style="text-decoration:none" onclick="window.parent.recordExternalClick('buy_coffee')">
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
    water_badge = f'<span class="click-badge">{st.session_state.click_stats["water_plant"]}</span>' if st.session_state.click_stats["water_plant"] > 0 else ""
    
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">{water_bubble_text}</div>
        <div class="plant-emoji" onclick="parent.document.getElementById('water_button').click()">
            🪴{water_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 隐形浇水触发器
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧", key="water_button", visible=False):
            record_click("water_plant")
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

# ==========================================
# 5. 处理外部链接点击记录
# ==========================================
# 检查URL参数或localStorage来记录外部点击
def check_external_clicks():
    # 这里可以扩展处理外部链接的点击记录
    # 例如通过URL参数、localStorage或sessionStorage
    pass

# ==========================================
# 6. 程序入口
# ==========================================
if __name__ == "__main__":
    check_external_clicks()
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
        
    # 定期保存统计数据
    save_click_stats()
