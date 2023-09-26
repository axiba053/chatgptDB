# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：
"""
import streamlit as st
from PIL import Image

def Version(v):
    st.markdown(v)

v0_1="""
## V0.1 (2023.08.06):
* 支持多种文件格式（txt/pdf/word/md）
* 本地数据库存储
* 可追加文件更新数据库
---
"""

v1_0="""
## V1.0 (2023.08.19):
* 网页可视化界面
* 云端数据库存储
* 增加账户管理(注册/登录/修改密码)
* 实现一个账户对应一个数据库
---
"""

v1_1="""
## V1.1 (2023.08.25):
* 修改密码需要邮箱和原密码
* 增加保存/清除API,切换页面后不需重新输入API
* 支持多文件同时上传
* 增加版本更新页面
* 增加Bilibili客服计划页面
---
"""

v1_2="""
## V1.2 (2023.09.26):
* 增加文本资料嵌入数据库时显示预计消费
* 增加提问时显示消耗token及消费金额
* 增加显示答案来源
* 增加多页面显示图标
* Bilibili客服计划数据库新增bilibili帮助页面内容
---
"""


image = Image.open('./image/AIgirl.png')
st.set_page_config(page_title='AI客服', layout='wide', page_icon=image)
st.header('版本更新:hammer_and_wrench:')
st.markdown('---')


Version(v1_2)
Version(v1_1)
Version(v1_0)
Version(v0_1)
