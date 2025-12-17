# ==========================================
# 3. 拦截与跳转逻辑 (增强版 - 修复不跳转问题)
# ==========================================
# 获取 URL 参数
query_params = st.query_params

if "target" in query_params:
    try:
        target_idx = int(query_params["target"])
        if 0 <= target_idx < len(GAME_DATA):
            key, zh_title, _, _, real_url = GAME_DATA[target_idx]
            
            # 1. 记录数据
            new_count = save_data_and_record(key, zh_title)
            
            # 2. 隐藏主界面，只显示跳转页
            st.markdown("""
            <style>
                .stApp > header {display:none;} 
                .stApp .main .block-container {padding-top:0; max-width:100%;}
            </style>
            """, unsafe_allow_html=True)
            
            # 3. 构建超级跳转 HTML
            # 逻辑：尝试自动跳 -> 失败则显示大按钮
            redirect_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                        display: flex; flex-direction: column; align-items: center; justify-content: center;
                        height: 100vh; margin: 0; background-color: #f9fafb;
                    }}
                    .loader {{
                        border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%;
                        width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 20px;
                    }}
                    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                    .btn {{
                        background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none;
                        border-radius: 8px; font-weight: 600; margin-top: 20px; transition: background 0.2s;
                    }}
                    .btn:hover {{ background-color: #1d4ed8; }}
                    .status {{ color: #6b7280; margin-bottom: 10px; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="loader"></div>
                <h3>正在前往: {zh_title}</h3>
                <div class="status">热度: {new_count} 🔥 | 记录成功</div>
                
                <script>
                    setTimeout(function() {{
                        // 尝试方法 1: 修改父窗口地址
                        try {{
                            window.top.location.href = "{real_url}";
                        }} catch(e) {{
                            console.log("方法1失败，尝试方法2");
                            // 尝试方法 2: 修改当前窗口地址
                            window.location.href = "{real_url}";
                        }}
                    }}, 800); // 延迟800毫秒，给用户看一眼提示，也等待浏览器准备好
                </script>
                
                <p style="margin-top:30px; font-size:13px; color:#999;">如果页面没有自动跳转，请点击下方按钮：</p>
                <a href="{real_url}" class="btn" target="_blank">点击前往 (Go) ➜</a>
            </body>
            </html>
            """
            
            # 渲染全屏跳转组件
            components.html(redirect_html, height=800, scrolling=False)
            
            # 给浏览器足够的时间执行 JS
            time.sleep(2.5) 
            st.stop()
            
    except ValueError:
        pass
