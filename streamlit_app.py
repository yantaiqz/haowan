import streamlit as st
import time
import json
import os
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. 全局配置与数据定义
# ==========================================
st.set_page_config(
    page_title="AI.找乐子 | AI.Fun",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 定义游戏数据 (ID, 中文标题, 描述, 图标, 真实URL)
# 我们需要给每个游戏一个唯一的 ID (key)，方便追踪
GAME_DATA = [
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

# 英文翻译映射
EN_TEXTS_MAP = {
    "wealth": ("Wealth Rankings", "Where do I stand?"),
    "rabbit": ("AI Rabbit", "One-click AI content detection"),
    "buffett": ("Buffett's Portfolio", "Evolution of Berkshire Hathaway"),
    "red": ("Red Stain", "State-owned investments data"),
    "world_house": ("Global Housing Prices", "Comparison of world city prices"),
    "cn_house": ("China Housing Market", "Urban housing price trends"),
    "million": ("Million Investment", "Return comparison of top products"),
    "lawyer": ("Intl Lawyer", "AI legal consultation worldwide"),
    "legal1000": ("Legal1000", "Global legal institution navigator"),
}

DATA_FILE = 'click_data.json'

# ==========================================
# 2. 数据处理逻辑 (加载与保存)
# ==========================================
def load_data():
    """加载数据到 session_state"""
    if 'click_counts' not in st.session_state:
        st.session_state.click_counts = {}
    if 'click_history' not in st.session_state:
        st.session_state.click_history = []
        
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.session_state.click_counts = data.get('click_counts', {})
                st.session_state.click_history = data.get('click_history', [])
        except Exception as e:
            print(f"加载失败: {e}")

def save_data_and_record(key, app_name):
    """记录点击并保存到文件"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. 更新计数
    if key not in st.session_state.click_counts:
        st.session_state.click_counts[key] = {'count': 0, 'app_name': app_name}
    
    st.session_state.click_counts[key]['count'] += 1
    st.session_state.click_counts[key]['last_clicked'] = now_str
    st.session_state.click_counts[key]['app_name'] = app_name # 确保名字是最新的

    # 2. 更新历史
    st.session_state.click_history.append({
        'timestamp': now_str,
        'key': key,
        'app_name': app_name,
        'language': st.session_state.get('language', 'zh')
    })
    # 只保留最近50条
    if len(st.session_state.click_history) > 50:
        st.session_state.click_history = st.session_state.click_history[-50:]

    # 3. 写入文件
    try:
        data_to_save = {
            'click_counts': st.session_state.click_counts,
            'click_history': st.session_state.click_history,
            'last_updated': now_str
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存失败: {e}")
        
    return st.session_state.click_counts[key]['count']

# 初始化数据
load_data()

# ==========================================
# 3. 拦截与跳转逻辑 (核心修复部分)
# ==========================================
# 获取 URL 参数
query_params = st.query_params

if "target" in query_params:
    try:
        target_idx = int(query_params["target"])
        if 0 <= target_idx < len(GAME_DATA):
            key, zh_title, _, _, real_url = GAME_DATA[target_idx]
            
            # 记录数据
            new_count = save_data_and_record(key, zh_title)
            
            # 执行跳转
            st.markdown(f"""
            <style>
                .stApp {{ display: none; }} /* 隐藏主界面，只显示跳转提示 */
            </style>
            """, unsafe_allow_html=True)
            
            redirect_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="refresh" content="0;url={real_url}">
            </head>
            <body>
                <script>
                    window.top.location.href = "{real_url}";
                </script>
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; color:#555;">
                    <h3>正在跳转 / Redirecting...</h3>
                    <p>{zh_title}</p>
                    <p>累计热度: {new_count} 🔥</p>
                </div>
            </body>
            </html>
            """
            components.html(redirect_html, height=800)
            time.sleep(1.0) # 给浏览器一点时间执行JS
            st.stop() # 停止渲染主页面
    except ValueError:
        pass

# ==========================================
# 4. 页面显示逻辑
# ==========================================

# 语言设置
if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'trigger_water' not in st.session_state:
    st.session_state.trigger_water = False

lang_texts = {
    'zh': {
        'page_title': 'AI.找乐子',
        'subtitle': '无聊而有趣的AI网页小应用',
        'top_right_btn': '✨ 获得新应用',
        'footer_title': '关于本站',
        'footer_text': '这里收录了我这些年做的一系列小玩意儿。它们算不上什么实用的东西，但玩起来都还挺有意思的。',
        'footer_creator': '老祁走❤️制作',
        'water_bubble': '已浇水 {count} 次',
    },
    'en': {
        'page_title': 'AI.Fun',
        'subtitle': 'Silly but fun AI web apps',
        'top_right_btn': '✨ Get new apps',
        'footer_title': 'About this site',
        'footer_text': 'This is a collection of silly little projects I\'ve made over the years. None of them are particularly useful, but they\'re all fun to play with.',
        'footer_creator': 'Made with ❤️ by LaoQi',
        'water_bubble': 'Watered {count} times',
    }
}
current_text = lang_texts[st.session_state.language]

# CSS 样式 (保留你原来的优美样式)
st.markdown("""
<style>
    :root { --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    * { font-family: var(--font-sans) !important; letter-spacing: -0.02em !important; }
    .stApp { background-color: #FFFFFF !important; color: #111827; }
    .block-container { padding-top: 1rem; max-width: 1200px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 按钮 */
    .neal-btn {
        background: white; border: 1px solid #e5e7eb; color: #1f2937;
        font-weight: 600; font-size: 14px; padding: 8px 16px; border-radius: 8px;
        cursor: pointer; transition: all 0.2s ease; width: 100%; height: 38px;
    }
    .neal-btn:hover { background: #f9fafb; transform: translateY(-1px); }
    .neal-btn-link { text-decoration: none; width: 100%; display: block; }
    
    /* 卡片 */
    .card-link { text-decoration: none; color: inherit; display: block; margin-bottom: 16px; }
    .neal-card {
        background-color: white; border-radius: 12px; padding: 20px;
        height: 100px; width: 100%; border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); display: flex; align-items: center; gap: 16px;
        transition: all 0.2s ease; position: relative;
    }
    .neal-card:hover { transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08); border-color: #d1d5db; }
    
    .card-icon { font-size: 32px; flex-shrink: 0; }
    .card-title { font-size: 1.125rem; font-weight: 700; color: #111827; line-height: 1.2; }
    .card-desc { font-size: 0.875rem; color: #6b7280; line-height: 1.3; }
    
    /* 点击计数角标 */
    .click-badge {
        position: absolute; top: 10px; right: 10px;
        background-color: #f3f4f6; color: #9ca3af;
        font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 600;
    }
    
    /* 标题与页脚 */
    .main-title { text-align: center; font-size: 3rem; font-weight: 900; margin-bottom: 8px; margin-top: -20px; }
    .subtitle { text-align: center; font-size: 1.125rem; color: #6b7280; margin-bottom: 40px; }
    .footer-area { margin: 60px auto 40px; padding-top: 32px; border-top: 1px solid #f3f4f6; text-align: center; }
    .footer-links { display: flex; gap: 12px; justify-content: center; width: 100%; margin: 16px 0; }
    .footer-creator { color: #9ca3af; font-size: 0.875rem; margin-top: 16px; }

    /* 浇水 */
    .plant-container { position: fixed; bottom: 20px; right: 20px; text-align: center; z-index: 999; }
    .water-bubble { background: white; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 6px; opacity: 0; transition: opacity 0.3s; }
    .show-bubble { opacity: 1; }
    .plant-emoji { font-size: 48px; cursor: pointer; transition: transform 0.2s ease; }
    .plant-emoji:hover { transform: scale(1.08); }
</style>
""", unsafe_allow_html=True)

def render_home():
    # 顶部
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

    # 游戏卡片网格
    cols = st.columns(3)
    for idx, (key, zh_title, zh_desc, icon, _) in enumerate(GAME_DATA):
        # 语言处理
        if st.session_state.language == 'zh':
            title, desc = zh_title, zh_desc
        else:
            title, desc = EN_TEXTS_MAP.get(key, (zh_title, zh_desc))
            
        # 获取计数
        count = st.session_state.click_counts.get(key, {}).get('count', 0)
        
        # 构造“拦截”链接：指向当前页面，带 target 参数
        # target="_self" 强制刷新当前页，触发 Python 的拦截逻辑
        intercept_url = f"./?target={idx}"
        
        with cols[idx % 3]:
            st.markdown(f"""
            <a href="{intercept_url}" target="_self" class="card-link">
                <div class="neal-card">
                    <div class="click-badge">🔥 {count}</div>
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
        <div style="font-weight:800; font-size:1.5rem; margin-bottom:8px; color:#1f2937;">{current_text['footer_title']}</div>
        <div style="color:#6b7280; margin-bottom:24px; max-width:500px; margin-left:auto; margin-right:auto;">{current_text['footer_text']}</div>
        <div class="footer-links">
            <a href="#" style="text-decoration:none"><button class="neal-btn">Newsletter 📰</button></a>
            <a href="#" style="text-decoration:none"><button class="neal-btn">Twitter 🐦</button></a>
            <a href="#" style="text-decoration:none"><button class="neal-btn">Buy Coffee ☕</button></a>
        </div>
        <div class="footer-creator">{current_text['footer_creator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 浇水
    water_bubble_text = current_text['water_bubble'].format(count=st.session_state.water_count)
    bubble_class = "show-bubble" if st.session_state.trigger_water else ""
    st.markdown(f"""
    <div class="plant-container">
        <div class="water-bubble {bubble_class}">{water_bubble_text}</div>
        <div class="plant-emoji">🪴</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 浇水隐形按钮
    c1, c2 = st.columns([10, 1])
    with c2:
        if st.button("💧"):
            st.session_state.water_count += 1
            st.session_state.trigger_water = True
            st.rerun()

# ==========================================
# 5. 管理员视图 (侧边栏)
# ==========================================
def show_admin_stats():
    if st.sidebar.checkbox("显示后台数据 (Admin)", key="show_stats"):
        st.sidebar.markdown("### 📊 排行榜")
        # 排序
        items = []
        for k, v in st.session_state.click_counts.items():
            items.append((v['app_name'], v['count']))
        items.sort(key=lambda x: x[1], reverse=True)
        
        for name, count in items:
            st.sidebar.markdown(f"**{name}**: {count} 次")
            
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 最近访问")
        for item in reversed(st.session_state.click_history[-10:]):
            st.sidebar.text(f"{item['timestamp']}\n{item['app_name']}")

if __name__ == "__main__":
    show_admin_stats()
    render_home()
    
    if st.session_state.trigger_water:
        time.sleep(1.5)
        st.session_state.trigger_water = False
        st.rerun()
