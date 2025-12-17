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
        height: 100px; 
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
# 4. 页面渲染逻辑
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
# 5. 程序入口
# ==========================================
if __name__ == "__main__":
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()


        
import sqlite3
import uuid  # <--- 新增导入
import datetime
import os
# 持久化目录（Streamlit Share 仅~/目录可持久化）
DB_DIR = os.path.expanduser("~/")
DB_FILE = os.path.join(DB_DIR, "visit_stats.db")
# -------------------------- 配置 --------------------------
#DB_FILE = "visit_stats.db"

def init_db():
    """初始化数据库（包含自动修复旧表结构的功能）"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    # 1. 确保表存在（这是旧逻辑）
    c.execute('''CREATE TABLE IF NOT EXISTS daily_traffic 
                 (date TEXT PRIMARY KEY, 
                  pv_count INTEGER DEFAULT 0)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS visitors 
                 (visitor_id TEXT PRIMARY KEY, 
                  first_visit_date TEXT)''')
    
    # 2. 【关键修复】手动检查并添加缺失的列 (Schema Migration)
    # 获取 visitors 表的所有列名
    c.execute("PRAGMA table_info(visitors)")
    columns = [info[1] for info in c.fetchall()]
    
    # 如果发现旧数据库里没有 last_visit_date，就动态添加进去
    if "last_visit_date" not in columns:
        try:
            c.execute("ALTER TABLE visitors ADD COLUMN last_visit_date TEXT")
            # 可选：把所有老数据的最后访问时间初始化为他们的首次访问时间，避免空值
            c.execute("UPDATE visitors SET last_visit_date = first_visit_date WHERE last_visit_date IS NULL")
        except Exception as e:
            print(f"数据库升级失败: {e}")

    conn.commit()
    conn.close()

def get_visitor_id():
    """获取或生成访客ID（修复版：使用UUID替代不稳定的内部API）"""
    if "visitor_id" not in st.session_state:
        # 生成一个唯一的随机ID，并保存在当前会话状态中
        st.session_state["visitor_id"] = str(uuid.uuid4())
    return st.session_state["visitor_id"]

def track_and_get_stats():
    """核心统计逻辑"""
    init_db()
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    today_str = datetime.datetime.utcnow().date().isoformat()
    visitor_id = get_visitor_id() # 这里调用修改后的函数

    # --- 写操作 (仅当本Session未计数时执行) ---
    if "has_counted" not in st.session_state:
        try:
            # 1. 更新每日PV
            c.execute("INSERT OR IGNORE INTO daily_traffic (date, pv_count) VALUES (?, 0)", (today_str,))
            c.execute("UPDATE daily_traffic SET pv_count = pv_count + 1 WHERE date=?", (today_str,))
            
            # 2. 更新访客UV信息
            c.execute("SELECT visitor_id FROM visitors WHERE visitor_id=?", (visitor_id,))
            exists = c.fetchone()
            
            if exists:
                c.execute("UPDATE visitors SET last_visit_date=? WHERE visitor_id=?", (today_str, visitor_id))
            else:
                c.execute("INSERT INTO visitors (visitor_id, first_visit_date, last_visit_date) VALUES (?, ?, ?)", 
                          (visitor_id, today_str, today_str))
            
            conn.commit()
            st.session_state["has_counted"] = True
            
        except Exception as e:
            st.error(f"数据库写入错误: {e}")

    # --- 读操作 ---
    # 1. 获取今日UV
    c.execute("SELECT COUNT(*) FROM visitors WHERE last_visit_date=?", (today_str,))
    today_uv = c.fetchone()[0]
    
    # 2. 获取历史总UV
    c.execute("SELECT COUNT(*) FROM visitors")
    total_uv = c.fetchone()[0]

    # 3. 获取今日PV
    c.execute("SELECT pv_count FROM daily_traffic WHERE date=?", (today_str,))
    res_pv = c.fetchone()
    today_pv = res_pv[0] if res_pv else 0
    
    conn.close()
    
    return today_uv, total_uv, today_pv

# -------------------------- 页面展示 --------------------------

# 执行统计
try:
    today_uv, total_uv, today_pv = track_and_get_stats()
except Exception as e:
    st.error(f"统计模块出错: {e}")
    today_uv, total_uv, today_pv = 0, 0, 0

# CSS 样式
st.markdown("""
<style>
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    .metric-box {
        text-align: center;
    }
    .metric-label {
        color: #6c757d;
        font-size: 0.85rem;
        margin-bottom: 2px;
    }
    .metric-value {
        color: #212529;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .metric-sub {
        font-size: 0.7rem;
        color: #adb5bd;
    }
    /* 优化右上角按钮样式 */
    div[data-testid="column"]:nth-child(2) button {
        width: 100%;
        white-space: nowrap;
        font-size: 0.85rem;
        padding: 4px 8px;
    }
    /* 确保HTML按钮和原生按钮样式一致 */
    div[data-testid="column"]:nth-child(3) button:hover {
        background-color: #0284c7;
    }
</style>
""", unsafe_allow_html=True)

# 展示数据
st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-sub">今日 UV: {today_uv} 访客数</div>
    </div>
    <div class="metric-box" style="border-left: 1px solid #dee2e6; border-right: 1px solid #dee2e6; padding-left: 20px; padding-right: 20px;">
        <div class="metric-sub">历史总 UV: {total_uv} 总独立访客</div>
    </div>
</div>
""", unsafe_allow_html=True)
