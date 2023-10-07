# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：根据提问查询数据库，将查询结果输入chatgpt输出答案
"""
from dotenv import load_dotenv
import streamlit as st
from ui import Ui
from authentica import UserInfos
from chatDB import create_collection

def main():
    if 'API' not in st.session_state:
        st.session_state['API'] = ''
    load_dotenv()
    Ui().side_bar()
    # interface_form=st.form('Interface')
    st.subheader('界面')
    menu = ["首页","注册","登录","修改密码","重置密码"]
    choice = st.selectbox("",menu)
    if choice =="首页":
        Ui().my_info()
    elif choice =="注册":
        username=UserInfos().register()
        if username:
            create_collection(username)
    elif choice =="登录":
        username=UserInfos().login()
        if username:
            st.markdown('---')
            Ui().main_interface(username)
    elif choice=="重置密码":
        UserInfos().forget_password()
    elif choice=="修改密码":
        username=st.session_state['username']
        UserInfos(username).change_password()

if __name__=="__main__":
    main()

