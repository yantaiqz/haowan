# 在原有代码基础上，在render_home函数中修改卡片部分：

# 游戏卡片网格
cols = st.columns(3)
for idx, (title, desc, icon, url) in enumerate(current_text['games']):
    with cols[idx % 3]:
        # 获取该URL的点击次数
        click_count = st.session_state.click_counts.get(url, {}).get('count', 0)
        
        # 创建按钮
        if st.button(
            label=f"{icon} {title}",
            key=f"btn_{url}",
            help=desc,
            use_container_width=True
        ):
            record_click(url)
            # 使用JavaScript打开新窗口
            st.markdown(f'<script>window.open("{url}", "_blank");</script>', unsafe_allow_html=True)
            st.rerun()
        
        # 显示描述和点击次数
        st.caption(f"{desc} • 👆 {click_count}次")
