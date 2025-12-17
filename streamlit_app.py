import streamlit as st
import time

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 状态初始化 ---
# 1. 浇水彩蛋状态
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

# 2. 语言状态
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 3. 点击统计状态 (以URL作为唯一键值)
if 'click_counts' not in st.session_state:
    st.session_state.click_counts = {}

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
        'click_label': '热度', # 新增：显示的标签
        'open_btn': '🚀 打开应用', # 新增：按钮文字
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
        'click_label': 'Clicks',
        'open_btn': '🚀 Launch',
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
# 3. 核心 CSS (优化版+计数器样式)
# ==========================================
st.markdown("""
<style>
    :root {
        --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        --color-gray-50: #f9fafb;
        --color-gray-100: #f3f4f6;
        --color-gray-200: #e5e7eb;
        --color-gray-300: #d1d5db;
        --color-gray-500: #6b7280;
        --color-gray-800: #1f2937;
        --color-gray-900: #111827;
        --color-accent: #6366f1; /* 增加一个强调色 */
    }

    * { font-family: var(--font-sans) !important; letter-spacing: -0.02em !important; }
    .stApp { background-color: #FFFFFF !important; color: var(--color-gray-900); }
    .block-container { padding-top: 1rem; max-width: 1200px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* 按钮样式重置 */
    .stButton > button {
        border-radius: 8px !important;
        border: 1px solid var(--color-gray-200) !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        width: 100%;
    }
    .stButton > button:hover {
        border-color: var(--color-gray-300) !important;
        background-color: var(--color-gray-50) !important;
        transform: translateY(-1px);
    }

    /* 顶部链接按钮 */
    .neal-btn {
        background: white; border: 1px solid var(--color-gray-200);
        color: var(--color-gray-800); font-weight: 600; font-size: 14px;
        padding: 8px 16px; border-radius: 8px; cursor: pointer;
        text-decoration: none; display: inline-flex; align-items: center; justify-content: center;
        width: 100%; height: 38px;
    }
    .neal-btn:hover { background: var(--color-gray-50); transform: translateY(-1px); }

    /* 标题样式 */
    .main-title { text-align: center; font-size: 3rem; font-weight: 900; margin-bottom: 8px; margin-top: -20px; line-height: 1.1; }
    .subtitle { text-align: center; font-size: 1.125rem; color: var(--color-gray-500); margin-bottom: 40px; }
    
    /* 卡片样式 (修改为纯展示，不可点击，点击由下方按钮触发) */
    .neal-card {
        background-color: white; 
        border-radius: 12px;
        padding: 20px;
        height: 100px; 
        width: 100%; 
        border: 1px solid var(--color-gray-200);
        display: flex; 
        flex-direction: row; 
        align-items: center; 
        gap: 16px;
        position: relative; /* 为计数器定位 */
    }
    .card-icon { font-size: 32px; flex-shrink: 0; }
    .card-content { flex-grow: 1; }
    .card-title { font-size: 18px; font-weight: 700; margin-bottom: 2px; line-height: 1.2; }
    .card-desc { font-size: 14px; color: var(--color-gray-500); line-height: 1.3; }
    
    /* 新增：热度徽章 */
    .fire-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        background-color: var(--color-gray-100);
        color: var(--color-gray-500);
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 2px;
    }

    /* Footer */
    .footer-area { max-width: 700px; margin: 60px auto 40px; padding-top: 32px; border-top: 1px solid var(--color-gray-100); text-align: center; }
    .footer-title { font-weight: 800; font-size: 1.5rem; margin-bottom: 8px; }
    .footer-text { color: var(--color-gray-500); margin: 0 auto 24px; line-height: 1.6; }
    .footer-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
    .footer-creator { color: var(--color-gray-400); font-size: 0.875rem; margin-top: 16px; }

    /* 浇水 */
    .plant-container { position: fixed; bottom: 20px; right: 20px; text-align: center; z-index: 999; }
    .water-bubble { background: white; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 6px; opacity: 0; transition: opacity 0.3s; }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 48px; cursor: pointer; transition: transform 0.2s; }
    .plant-emoji:hover { transform: scale(1.08); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 逻辑处理函数
# ==========================================
def open_url_js(url):
    """
    生成一段JS代码，用于在不跳转的情况下打开新标签页，
    通常在 st.button 点击后调用。
    """
    js = f"""
    <script>
        window.open("{url}", "_blank");
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# ==========================================
# 5. 页面渲染逻辑
# ==========================================
def render_home():
    # 顶部导航
    c_spacer, c_lang, c_link = st.columns([10, 1.2, 1.8])
    with c_lang:
        lang_btn_text = "English" if st.session_state.language == 'zh' else "中文"
        if st.button(lang_btn_text, key="lang_switch_main"):
            st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
            st.rerun()
    with c_link:
        st.markdown(f"""<a href="https://neal.fun/newsletter/" target="_blank" style="text-decoration:none"><button class="neal-btn">{current_text['top_right_btn']}</button></a>""", unsafe_allow_html=True)

    # 标题
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # --- 游戏卡片网格 (核心修改部分) ---
    cols = st.columns(3)
    
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            # 1. 获取当前URL的点击数
            clicks = st.session_state.click_counts.get(url, 0)
            
            # 2. 渲染静态的卡片UI (移除 <a> 标签，增加计数 Badge)
            st.markdown(f"""
            <div class="neal-card">
                <div class="fire-badge">🔥 {current_text['click_label']} {clicks}</div>
                <div class="card-icon">{icon}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. 使用 Streamlit 原生按钮处理点击逻辑
            # 为了布局紧凑，我们在卡片下方放一个全宽按钮
            if st.button(f"{current_text['open_btn']}", key=f"btn_{idx}"):
                # 逻辑A: 计数 +1
                st.session_state.click_counts[url] = clicks + 1
                # 逻辑B: 执行 JS 打开新页面
                open_url_js(url)
                # 逻辑C: 稍微延迟后重载页面以更新 UI 上的数字
                time.sleep(0.5) 
                st.rerun()
            
            # 增加一点间距
            st.write("")

    # Footer
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
    st.markdown(f"""<div class="plant-container"><div class="water-bubble {bubble_class}">{water_bubble_text}</div><div class="plant-emoji">🪴</div></div>""", unsafe_allow_html=True)
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
