# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：
"""
import streamlit as st
from PIL import Image


image = Image.open('./image/AIgirl.png')
st.set_page_config(page_title='AI客服', layout='wide', page_icon=image)
st.title('B站客服📺')
image1 = Image.open("./image/2233.png")
st.sidebar.image(image1, caption="", width=200)


info="""
---
道友们好，我将[百度百科](https://baike.baidu.com/item/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9/8018053?fromtitle=bilibili&fromid=7056160&fromModule=lemma_search-box)
及[bilibili帮助页面](https://www.bilibili.com/blackboard/help.html)中B站相关内容上传数据库，搭建了一个B站AI客服系统:seedling:。

可供大家提问调戏，关联账号密码在后面:hibiscus:。

欢迎大家踊跃上传更新B站相关内容，共同完善B站客服系统:two_hearts:。我也一定会尽力维护下去:punch:！

---
"""


user="""
###### 使用以下账号密码登录即可上传B站相关文件或提问
> 账号：**bilibili**   
> 密码：**123456**
"""
st.balloons()
st.markdown(info)
st.markdown(user)

