import streamlit as st
import time
import json
from datetime import datetime
import webbrowser

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
# 2. 点击次数跟踪功能
# ==========================================
def init_click_counts():
    """初始化所有按钮的点击次数"""
    if 'click_counts' not in st.session_state:
        # 获取所有URL（包括两种语言的）
        all_urls = set()
        for lang in ['zh', 'en']:
            for _, _, _, url in lang_texts[lang]['games']:
                all_urls.add(url)
        
        # 初始化点击次数
        st.session_state.click_counts = {}
        for url in all_urls:
            st.session_state.click_counts[url] = {
                'count': 0,
                'last_clicked': None,
                'app_name': get_app_name_by_url(url)
            }
        
        # 初始化点击历史记录
        st.session_state.click_history = []

def get_app_name_by_url(url):
    """根据URL获取应用名称"""
    for lang in ['zh', 'en']:
        for title, desc, icon, app_url in lang_texts[lang]['games']:
            if app_url == url:
                return f"{icon} {title}"
    return "未知应用"

def record_click(url):
    """记录按钮点击"""
    if url not in st.session_state.click_counts:
        st.session_state.click_counts[url] = {
            'count': 0,
            'last_clicked': None,
            'app_name': get_app_name_by_url(url)
        }
    
    # 更新点击次数
    st.session_state.click_counts[url]['count'] += 1
    st.session_state.click_counts[url]['last_clicked'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 记录点击历史
    st.session_state.click_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'url': url,
        'app_name': st.session_state.click_counts[url]['app_name'],
        'language': st.session_state.language
    })
    
    # 限制历史记录长度
    if len(st.session_state.click_history) > 100:
        st.session_state.click_history = st.session_state.click_history[-100:]
    
    # 保存到本地文件（可选）
    save_click_data()
    
    # 打开链接
    webbrowser.open_new_tab(url)
    st.session_state.open_url = url

def save_click_data():
    """保存点击数据到文件"""
    try:
        data = {
            'click_counts': st.session_state.click_counts,
            'click_history': st.session_state.click_history[-50:],  # 只保存最近50条
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open('click_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据失败: {e}")

def load_click_data():
    """从文件加载点击数据"""
    try:
        with open('click_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'click_counts' in data:
                st.session_state.click_counts = data['click_counts']
            if 'click_history' in data:
                st.session_state.click_history = data['click_history']
    except FileNotFoundError:
        print("未找到历史数据文件，将创建新的记录")
    except Exception as e:
        print(f"加载数据失败: {e}")

def show_click_stats():
    """显示点击统计信息（管理员视图）"""
    if st.sidebar.checkbox("显示点击统计", key="show_stats"):
        st.sidebar.markdown("### 📊 点击统计")
        
        # 按点击次数排序
        sorted_counts = sorted(
            st.session_state.click_counts.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        # 显示前10个
        for i, (url, data) in enumerate(sorted_counts[:10]):
            app_name = data['app_name']
            count = data['count']
            last_clicked = data.get('last_clicked', '从未')
            
            st.sidebar.markdown(f"""
            **{i+1}. {app_name}**
            - 点击次数: **{count}** 次
            - 最后点击: {last_clicked}
            """)
        
        # 显示总计
        total_clicks = sum(data['count'] for data in st.session_state.click_counts.values())
        st.sidebar.markdown(f"**总计点击次数:** {total_clicks} 次")
        
        # 显示最近点击历史
        if st.sidebar.checkbox("显示最近点击历史"):
            st.sidebar.markdown("### 📋 最近点击")
            for item in reversed(st.session_state.click_history[-10:]):
                st.sidebar.markdown(f"**{item['app_name']}**")
                st.sidebar.markdown(f"时间: {item['timestamp']}")
                st.sidebar.markdown("---")

# ==========================================
# 3. 多语言文本配置
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

# ==========================================
# 4. 初始化状态
# ==========================================
# 初始化语言状态
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 初始化浇水状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# 初始化打开URL状态
if 'open_url' not in st.session_state:
    st.session_state.open_url = None

# 初始化点击次数
init_click_counts()

# 尝试加载历史数据
load_click_data()

current_text = lang_texts[st.session_state.language]

# ==========================================
# 5. 核心 CSS (现代字体优化版)
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

    /* 3. 游戏卡片按钮样式 */
    .card-button {
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
        cursor: pointer;
        text-align: left;
    }
    .card-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); 
        border-color: var(--color-gray-300);
    }
    
    .card-click-counter {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        font-size: var(--text-xs);
        padding: 2px 6px;
        border-radius: 10px;
        font-weight: var(--font-semibold);
        z-index: 10;
        opacity: 0.8;
        transition: opacity 0.2s;
    }
    .card-button:hover .card-click-counter {
        opacity: 1;
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. 页面渲染逻辑
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
    
    # 游戏卡片网格 - 使用按钮代替链接
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            # 获取该URL的点击次数
            click_count = st.session_state.click_counts.get(url, {}).get('count', 0)
            
            # 创建卡片按钮
            if st.button(
                label="",
                key=f"card_btn_{idx}",
                help=f"点击访问: {title}"
            ):
                record_click(url)
                st.rerun()
            
            # 使用HTML渲染卡片内容
            st.markdown(f"""
            <div class="card-button" onclick="document.getElementById('card_btn_{idx}').click()">
                <div class="card-click-counter">👆 {click_count}</div>
                <div class="card-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                </div>
            </div>
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
# 8. 程序入口
# ==========================================
if __name__ == "__main__":
    # 显示点击统计（侧边栏）
    show_click_stats()
    
    # 渲染主页面
    render_home()
    
    # 处理浇水动画
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
