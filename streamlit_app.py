import streamlit as st
import time
import json
import os
import streamlit.components.v1 as components

# ==========================================
# 0. 数据持久化逻辑 (新增)
# ==========================================
DATA_FILE = "click_stats.json"

def load_clicks():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_click(url_key):
    data = load_clicks()
    # 如果该链接没记录过，初始化为0
    if url_key not in data:
        data[url_key] = 0
    data[url_key] += 1
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data[url_key]

# ==========================================
# 1. 全局配置与重定向拦截 (关键修改)
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------
# 定义所有链接数据 (移到前面以便拦截逻辑调用)
# ------------------------------------------
GAME_LINKS = [
    # (Key/ID, 中文标题, 描述, 图标, 真实URL)
    ("wealth", "财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
    ("rabbit", "AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
    ("buffett", "巴菲特的组合", "伯克希尔·哈撒韦投资组合演变", "📈", "https://buffett.streamlit.app/"),
    ("red", "染红", "国资投资A股的数据可视化", "🔴", "https://ranhong.streamlit.app/"),
    ("world_house", "世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
    ("cn_house", "中国房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
    ("million", "百万投资", "顶尖理财产品的回报率对比", "💹", "https://nblawyer.streamlit.app/"),
    ("lawyer", "国际律师", "各国AI法律咨询和合同审查", "⚖️", "https://chuhai.streamlit.app/"),
    ("legal1000", "Legal1000", "全球法律与合规机构导航", "📚", "https://iterms.streamlit.app/"),
]

# ------------------------------------------
# 拦截逻辑：检查 URL 参数
# ------------------------------------------
# 获取查询参数 (兼容不同 Streamlit 版本)
query_params = st.query_params 

if "target" in query_params:
    target_index = int(query_params["target"])
    
    if 0 <= target_index < len(GAME_LINKS):
        key, _, _, _, real_url = GAME_LINKS[target_index]
        
        # 1. 记录点击
        new_count = save_click(key)
        
        # 2. 执行 JS 跳转 (使用 window.open 或 window.location)
        # 注意：meta refresh 也是一种备选，但 JS 更快
        redirect_html = f"""
        <script>
            // 稍微延迟一点点确保文件写入完成（通常不需要，但为了保险）
            window.top.location.href = "{real_url}";
        </script>
        <div style="text-align:center; padding-top: 50px;">
            <h3>正在跳转... / Redirecting...</h3>
            <p>已累计点击 / Total Clicks: {new_count}</p>
        </div>
        """
        components.html(redirect_html, height=200)
        st.stop() # 停止渲染后续页面，专注于跳转

# ==========================================
# 2. 状态与文本初始化
# ==========================================
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False
if 'language' not in st.session_state:
    st.session_state.language = 'zh' 

# 加载最新的点击数据用于显示
current_clicks = load_clicks()

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
        'click_label': '热度'
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
        'click_label': 'Clicks'
    }
}

current_text = lang_texts[st.session_state.language]

# ==========================================
# 3. 核心 CSS (保持原有优美样式，微调点击数显示)
# ==========================================
st.markdown("""
<style>
    :root {
        --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        --text-sm: 0.875rem;
        --text-lg: 1.125rem;
        --text-5xl: 3rem;
        --color-gray-50: #f9fafb;
        --color-gray-200: #e5e7eb;
        --color-gray-500: #6b7280;
        --color-gray-900: #111827;
    }
    * { font-family: var(--font-sans) !important; letter-spacing: -0.02em !important; }
    .stApp { background-color: #FFFFFF !important; color: var(--color-gray-900); }
    .block-container { padding-top: 1rem; max-width: 1200px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* 按钮与卡片样式 */
    .neal-btn {
        background: white; border: 1px solid var(--color-gray-200); color: #1f2937;
        font-weight: 600; font-size: 14px; padding: 8px 16px; border-radius: 8px;
        cursor: pointer; transition: all 0.2s ease; width: 100%; height: 38px;
    }
    .neal-btn:hover { background: var(--color-gray-50); transform: translateY(-1px); }
    
    .card-link { text-decoration: none; color: inherit; display: block; margin-bottom: 16px; }
    .neal-card {
        background-color: white; border-radius: 12px; padding: 20px;
        height: 100px; width: 100%; border: 1px solid var(--color-gray-200);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); display: flex; align-items: center; gap: 16px;
        transition: all 0.2s ease; position: relative; /* 为了定位点击数 */
    }
    .neal-card:hover { transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); }
    
    .card-icon { font-size: 32px; flex-shrink: 0; }
    .card-title { font-size: var(--text-lg); font-weight: 700; color: var(--color-gray-900); line-height: 1.2; }
    .card-desc { font-size: var(--text-sm); color: var(--color-gray-500); line-height: 1.3; }
    
    /* 新增：点击计数样式 */
    .click-badge {
        position: absolute; top: 10px; right: 10px;
        background-color: #f3f4f6; color: #9ca3af;
        font-size: 10px; padding: 2px 6px; border-radius: 4px;
        font-weight: 500;
    }

    .main-title { text-align: center; font-size: var(--text-5xl); font-weight: 900; margin-bottom: 8px; margin-top: -20px; }
    .subtitle { text-align: center; font-size: var(--text-lg); color: var(--color-gray-500); margin-bottom: 40px; }
    
    .footer-area { margin: 60px auto 40px; padding-top: 32px; border-top: 1px solid #f3f4f6; text-align: center; display: flex; flex-direction: column; align-items: center; }
    .footer-links { display: flex; gap: 12px; justify-content: center; width: 100%; margin: 16px 0; }
    
    .plant-container { position: fixed; bottom: 20px; right: 20px; text-align: center; z-index: 999; }
    .water-bubble { background: white; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 6px; opacity: 0; transition: opacity 0.3s; }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 48px; cursor: pointer; transition: transform 0.2s ease; }
    .plant-emoji:hover { transform: scale(1.08); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 页面渲染逻辑
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
        st.markdown(f"""
        <a href="https://neal.fun/newsletter/" target="_blank" class="neal-btn-link">
            <button class="neal-btn">{current_text['top_right_btn']}</button>
        </a>
        """, unsafe_allow_html=True)

    # 标题
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)
    
    # --- 游戏卡片网格 (使用 GAME_LINKS 数据) ---
    cols = st.columns(3)
    
    # 英文模式下，我们需要把 GAME_LINKS 映射成英文文本
    # 注意：这里为了简化，我直接在 loop 里做中英文判断
    # 实际项目中建议把 GAME_LINKS 的结构做得更像 lang_texts 那样支持多语言
    
    # 英文标题映射 (手动补全英文对应关系)
    en_titles = [
        "Wealth Rankings", "AI Rabbit", "Buffett's Portfolio", "Red Stain",
        "Global Housing Prices", "China Housing Market", "Million-Dollar Investment",
        "International Lawyer", "Legal1000"
    ]
    en_descs = [
        "Where do I stand?", "One-click AI content detection", "Evolution of Berkshire Hathaway", 
        "State-owned investments data", "Comparison of world city prices", "Urban housing price trends",
        "Return comparison of top products", "AI legal consultation worldwide", "Global legal institution navigator"
    ]

    for idx, (key, zh_title, zh_desc, icon, real_url) in enumerate(GAME_LINKS):
        # 决定显示的文本
        if st.session_state.language == 'zh':
            title = zh_title
            desc = zh_desc
        else:
            title = en_titles[idx]
            desc = en_descs[idx]
            
        # 获取点击数
        click_count = current_clicks.get(key, 0)
        
        # 构造内部跳转链接：指向自己，但带上 target 参数
        # target="_self" 强制在当前标签页刷新，触发 Streamlit 重新运行并进入拦截逻辑
        internal_link = f"./?target={idx}"
        
        with cols[idx % 3]:
            st.markdown(f"""
            <a href="{internal_link}" target="_self" class="card-link">
                <div class="neal-card">
                    <div class="click-badge">🔥 {click_count}</div>
                    <div class="card-icon">{icon}</div>
                    <div class="card-content">
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div class="footer-area">
        <div class="footer-title">{current_text['footer_title']}</div>
        <div class="footer-text">{current_text['footer_text']}</div>
        <div class="footer-links">
            <a href="#" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn1']}</button></a>
            <a href="#" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn2']}</button></a>
            <a href="#" style="text-decoration:none"><button class="neal-btn">{current_text['footer_btn3']}</button></a>
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

    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

if __name__ == "__main__":
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
