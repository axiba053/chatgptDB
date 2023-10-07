#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author      : xueqiang.liu
@contact     : liuxq@avatarget.com.cn
@Date        : 2023/8/16
@Description :
'''
import streamlit as st
import streamlit_authenticator_self as stauth
import yaml
from yaml.loader import SafeLoader
from ui import Ui

#hashed_passwords = stauth.Hasher(['abc']).generate()
# print(hashed_passwords)

class UserInfos:
    def __init__(self,username=''):
        self.username=username
        with open('config.yaml') as file:
            self.config = yaml.load(file, Loader=SafeLoader)
        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['preauthorized']
        )

    def updata_config(self):
        with open('config.yaml', 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
        st.success('信息已更新！')

    def register(self):
        try:
            Username= self.authenticator.register_user('注册界面', preauthorization=False)
            if Username:
                st.success(f'用户名：{Username}')
                self.updata_config()
                return Username
        except Exception as e:
            st.error(e)

    def login(self):
        name, authentication_status, Username = self.authenticator.login('登录界面', 'main')
        if st.session_state["authentication_status"]:
            st.write(f'**「{st.session_state["name"]}」** 欢迎使用～')
            self.authenticator.logout('点击退出登录', 'main', key='unique_key')
            return Username
        elif st.session_state["authentication_status"] is False:
            st.error('用户名/密码错误！')
        elif st.session_state["authentication_status"] is None:
            st.warning('请输入账号密码')

    def change_password(self):
        if st.session_state["authentication_status"]:
            try:
                if self.authenticator.reset_password(self.username, '修改密码界面'):
                    st.success('密码修改成功！')
                    self.updata_config()
            except Exception as e:
                st.error(e)
        else:
            st.warning('请先登录')

    def forget_password(self):
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = self.authenticator.forgot_password('重置密码界面')
            print(username_of_forgotten_password, email_of_forgotten_password, new_random_password)
            if username_of_forgotten_password:
                st.success('密码已重置为「123456」，请及时修改密码！')
                self.updata_config()
                # Random password should be transferred to user securely
            else:
                st.warning('请输入用户名及注册邮箱')
        except Exception as e:
            st.error(e)

    def forget_username(self):
        try:
            username_of_forgotten_username, email_of_forgotten_username = self.authenticator.forgot_username('Forgot username')
            print(username_of_forgotten_username, email_of_forgotten_username)
            if username_of_forgotten_username:
                st.success('Username to be sent securely')
                # Username should be transferred to user securely
            else:
                st.error('Email not found')
        except Exception as e:
            st.error(e)

    def updata_detail(self):
        if st.session_state["authentication_status"]:
            try:
                if self.authenticator.update_user_details(self.username, 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)
        self.updata_config()

