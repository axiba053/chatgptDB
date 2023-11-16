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
txCloud=":partly_sunny: [云服务器推荐](https://curl.qcloud.com/AlTN7fIG)"


image = Image.open('./image/AIgirl.png')
st.set_page_config(page_title='三强的小屋', layout='wide', page_icon=image)

st.markdown(website)
st.markdown(txCloud)
st.markdown(airport)


sub = st.button('ChatGPT官方账号免费分享及其他福利')
if sub:
    st.success('Bilibili扫码关注，回复口令「福利」自动获取')
    image1 = Image.open("./image/B.jpg")
    st.image(image1, caption="", width=200)
