import streamlit as st
import sqlite3
import uuid
import datetime
import os

# ==========================================
# 1. 全局配置
# ==========================================
st.set_page_config(
    page_title="80后老登的工具箱 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化所有状态
for key, default in {
    'language': 'zh',
    # 注意：不再需要 modal_open 这种开关变量了
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==========================================
# 2. 多语言文本配置
# ==========================================
lang_texts = {
    'zh': {
        'page_title': '80后老登的工具箱',
        'subtitle': '守住底裤的 AI 网页小应用',
        'top_right_btn': '✨ 获得新应用',
        'coffee_title': '请老登喝杯咖啡 ☕',
        'coffee_desc': '如果这些小工具让你感到有趣，欢迎支持老登的创作。',
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_btn1': '订阅新应用 📰',
        'footer_btn2': '关注老登公众号 🐦',
        'footer_btn3': '请老登一杯咖啡 ☕', 
        'footer_creator': '老祁走 ❤️ 制作',
        'qrcode_title': '扫码关注，获取新应用',
        'qrcode_desc': '第一时间获取最新应用更新',
        'games': [
            ("财富榜", "我能排第几", "💰", "https://youqian.streamlit.app/"),
            ("AI兔子", "一键检测AI内容痕迹", "🐰", "https://aituzi.streamlit.app/"),
            ("巴菲特", "伯克希尔投资演变", "📈", "https://buffett.streamlit.app/"),
            ("染红", "国资投资A股可视化", "🔴", "https://ranhong.streamlit.app/"),
            ("世界房价", "世界城市房价对比", "🌍", "https://fangchan.streamlit.app/"),
            ("中国房市", "城区房市价格趋势", "🏙️", "https://fangjia.streamlit.app/"),
            ("百万投资", "顶尖理财回报对比", "💹", "https://nblawyer.streamlit.app/"),
            ("国际律师", "全球AI法律咨询", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "全球合规机构导航", "📚", "https://iterms.streamlit.app/"),
        ]
    },
    'en': {
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'top_right_btn': '✨ Get apps',
        'coffee_title': 'Buy me a coffee ☕',
        'coffee_desc': 'If you find these tools helpful, consider supporting my work!',
        'footer_title': 'About this site',
        'footer_text': 'A collection of silly little projects. Not particularly useful, but fun to play with.',
        'footer_btn1': 'Newsletter 📰',
        'footer_btn2': 'Follow Me 🐦',
        'footer_btn3': 'Support Me ☕',
        'footer_creator': 'Made with ❤️ by LaoQi',
        'qrcode_title': 'Scan to Follow',
        'qrcode_desc': 'Get the latest app updates',
        'games': [
            ("Wealth", "Where do I stand?", "💰", "https://youqian.streamlit.app/"),
            ("AI Rabbit", "Content detection", "🐰", "https://aituzi.streamlit.app/"),
            ("Buffett", "Investment evolution", "📈", "https://buffett.streamlit.app/"),
            ("Red Stain", "State investment", "🔴", "https://ranhong.streamlit.app/"),
            ("Housing", "Global price comparison", "🌍", "https://fangchan.streamlit.app/"),
            ("China Home", "Urban price trends", "🏙️", "https://fangjia.streamlit.app/"),
            ("Million Invest", "Financial returns", "💹", "https://nblawyer.streamlit.app/"),
            ("AI Lawyer", "Global legal consultation", "⚖️", "https://chuhai.streamlit.app/"),
            ("Legal1000", "Global Compliance", "📚", "https://iterms.streamlit.app/"),
        ]
    }
}
current_text = lang_texts[st.session_state.language]

# ==========================================
# 3. 核心 CSS (Neal.fun 风格)
# ==========================================
st.markdown(f"""
<style>
    /* 基础重置 */
    .stApp {{ background-color: #FFFFFF !important; }}
    .block-container {{ padding-top: 2rem; max-width: 1000px !important; }}
    
    /* 隐藏多余组件 */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    /* 标题排版 */
    .main-title {{
        text-align: center; font-size: 3.5rem; font-weight: 900;
        letter-spacing: -0.1rem; color: #111; margin-bottom: 0.5rem;
    }}
    .subtitle {{
        text-align: center; font-size: 1.25rem; color: #666;
        margin-bottom: 3.5rem; font-weight: 400;
    }}

    /* 卡片布局优化 */
    .neal-card {{
        background: white; border-radius: 16px; padding: 1.5rem;
        height: 120px; border: 1px solid #e5e7eb;
        display: flex; align-items: center; gap: 1.2rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none !important; margin-bottom: 1rem;
    }}
    .neal-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.06);
        border-color: #d1d5db;
    }}
    .card-icon {{ font-size: 2.5rem; }}
    .card-title {{ font-weight: 700; font-size: 1.15rem; color: #111; }}
    .card-desc {{ font-size: 0.9rem; color: #6b7280; margin-top: 2px; }}

    /* Footer 按钮样式对齐 */
    .stButton > button {{
        background: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: #f9fafb !important;
        border-color: #d1d5db !important;
        transform: translateY(-1px);
    }}

    /* 底部统计容器 */
    .metric-container {{
        display: flex; justify-content: center; gap: 2rem;
        margin-top: 4rem; padding: 2rem 0;
        border-top: 1px solid #f3f4f6;
        color: #9ca3af; font-size: 0.85rem;
    }}

    /* 侧边浇水彩蛋 */
    .plant-container {{ position: fixed; bottom: 30px; right: 30px; z-index: 100; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 数据库与统计逻辑 (合并整理)
# ==========================================
# 持久化目录
DB_DIR = os.path.expanduser("~/")
DB_FILE = os.path.join(DB_DIR, "visit_stats.db")

def init_db():
    """初始化数据库（包含自动修复旧表结构的功能）"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    # 确保表存在
    c.execute('''CREATE TABLE IF NOT EXISTS daily_traffic 
                 (date TEXT PRIMARY KEY, pv_count INTEGER DEFAULT 0)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS visitors 
                 (visitor_id TEXT PRIMARY KEY, first_visit_date TEXT)''')
    
    # Schema Migration: 检查并添加 last_visit_date
    c.execute("PRAGMA table_info(visitors)")
    columns = [info[1] for info in c.fetchall()]
    
    if "last_visit_date" not in columns:
        try:
            c.execute("ALTER TABLE visitors ADD COLUMN last_visit_date TEXT")
            c.execute("UPDATE visitors SET last_visit_date = first_visit_date WHERE last_visit_date IS NULL")
        except Exception as e:
            print(f"数据库升级警告: {e}")

    conn.commit()
    conn.close()

def get_visitor_id():
    """获取或生成访客ID"""
    if "visitor_id" not in st.session_state:
        st.session_state["visitor_id"] = str(uuid.uuid4())
    return st.session_state["visitor_id"]

def track_and_get_stats():
    """核心统计逻辑"""
    init_db()
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    
    today_str = datetime.datetime.utcnow().date().isoformat()
    visitor_id = get_visitor_id()

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

# ==========================================
# 5. 定义原生弹窗 (st.dialog)
# ==========================================

# --- 公众号弹窗 ---
@st.dialog("扫码关注，获取新应用")
def show_qrcode_window():
    # 使用 columns 居中图片
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("qrcode_for_gh.jpg", use_container_width=True)
    
    st.markdown(f"""
        <div style='text-align:center; margin-top:10px; color:#666;'>
            {lang_texts[st.session_state.language]['qrcode_desc']}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("完成", use_container_width=True):
        st.rerun()

# --- 咖啡赞赏弹窗 (包含计算逻辑) ---
@st.dialog("请老登喝杯咖啡吧 ☕")
def show_coffee_window():
    # 1. 描述文本
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:15px; color:#444; font-size:0.95rem;'>
            {lang_texts[st.session_state.language]['coffee_desc']}
        </div>
    """, unsafe_allow_html=True)

    # 2. 初始化数量状态 (局部状态管理)
    if 'coffee_num' not in st.session_state:
        st.session_state.coffee_num = 1

    # 回调函数
    def set_coffee(num):
        st.session_state.coffee_num = num

    # 3. 快速选择按钮
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("🍺 1杯", use_container_width=True, on_click=set_coffee, args=(1,))
    with c2:
        st.button("🍺 3杯", use_container_width=True, on_click=set_coffee, args=(3,))
    with c3:
        st.button("🍺 5杯", use_container_width=True, on_click=set_coffee, args=(5,))

    # 4. 数字输入框 (双向绑定)
    count = st.number_input(
        "自定义数量 (杯)", 
        min_value=1, 
        max_value=100, 
        step=1, 
        key='coffee_num'
    )
    
    # 5. 计算金额与展示
    total_price = count * 10
    st.markdown(f"""
        <div style='text-align:center; margin: 15px 0; padding: 15px; background-color:#f8f9fa; border-radius:12px; border:1px solid #eee;'>
            <div style="font-size:0.9rem; color:#666;">支持 {count} 杯需</div>
            <div style="font-size:2.4rem; font-weight:800; color:#d9534f; line-height:1.2;">¥ {total_price}</div>
        </div>
    """, unsafe_allow_html=True)

    # 6. 收款码
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        # 记得确保目录下有这个图片
        try:
            st.image("wechat_pay.jpg", use_container_width=True)
        except:
            st.error("图片加载失败")

    st.write("")

# ==========================================
# 6. 主渲染逻辑
# ==========================================
def render_home():
    # --- 1. 顶部导航 ---
    t_col1, t_col2 = st.columns([8, 2])
    with t_col2:
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            l_btn = "En" if st.session_state.language == 'zh' else "中"
            if st.button(l_btn):
                st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'
                st.rerun()
        with inner_col2:
            if st.button("✨"):
                show_qrcode_window() # 直接调用

    # --- 2. 标题区 ---
    st.markdown(f'<div class="main-title">{current_text["page_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{current_text["subtitle"]}</div>', unsafe_allow_html=True)

    # --- 3. 卡片网格 ---
    cols = st.columns(3)
    for idx, (title, desc, icon, url) in enumerate(current_text['games']):
        with cols[idx % 3]:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none">
                <div class="neal-card">
                    <div class="card-icon">{icon}</div>
                    <div>
                        <div class="card-title">{title}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # --- 4. Footer 区域 ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; max-width:600px; margin: 0 auto;">
        <h2 style="font-weight:800; font-size:1.8rem;">{current_text['footer_title']}</h2>
        <p style="color:#666; line-height:1.6; margin: 1.5rem 0;">{current_text['footer_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    f_btns = st.columns([1,1,1,1])
    with f_btns[1]:
        if st.button(current_text['footer_btn2']): 
            show_qrcode_window() # 直接调用
            
    with f_btns[2]:
        if st.button(current_text['footer_btn3']): 
            show_coffee_window() # 直接调用

    # --- 5. 统计与彩蛋 ---
    try:
        today_uv, total_uv, today_pv = track_and_get_stats()
    except Exception as e:
        # 防止数据库错误导致页面崩坏
        today_uv, total_uv, today_pv = 0, 0, 0
    
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
    
    # 浇水彩蛋
    st.markdown(f'<div class="plant-container"><span style="font-size:3rem; cursor:pointer">🪴</span></div>', unsafe_allow_html=True)

# ==========================================
# 7. 入口
# ==========================================
if __name__ == "__main__":
    render_home()
