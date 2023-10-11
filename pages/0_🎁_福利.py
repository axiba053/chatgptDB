# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：
"""
import streamlit as st
from PIL import Image

airport="✈️  [魔法上网机场推荐](https://github.com/axiba053/ChatGPT-airport-tizi-fanqiang)"
website=":flag-cn:  [ChatGPT国内镜像网站推荐](https://github.com/axiba053/awesome-free-chatgpt/tree/main)"

fuli="ChatGPT/claude2官方账号免费分享"

st.markdown(website)
st.markdown(airport)


sub = st.button('ChatGPT/claude2官方账号免费分享')
if sub:
    st.success('Bilibili扫码关注，回复口令「福利」自动获取')
    image1 = Image.open("./image/B.jpg")
    st.image(image1, caption="", width=200)