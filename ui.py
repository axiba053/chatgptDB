# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：根据提问查询数据库，将查询结果输入chatgpt输出答案
"""
import os

from langchain.callbacks import get_openai_callback
import streamlit as st
from PIL import Image
from createDB import CreateDB
from chatDB import get_chain
import pathlib

import langchain
langchain.debug = True

class Ui:
    def side_bar(self):
        # 标题 图标
        image = Image.open('./image/AIgirl.png')
        st.set_page_config(page_title='AI客服', layout='wide', page_icon=image)
        st.header('AI智能客服💁')
        #左边栏
        with st.sidebar:
            st.image(image, caption="", width=50)
            st.markdown("## 客服使用说明")
            st.markdown("0. 首先注册/登陆")
            st.markdown("1. 填入OpenAI API-key")
            st.markdown("2. 上传资料文件，创建/更新数据库")
            st.markdown("3. 选择数据库提问")
            st.markdown("---")
            st.markdown("## 作者简介")
            st.markdown("大家好，这里是:blue[《三强的小屋》]！")
            st.write("作为知识的搬运工，我会持续更新AI相关技术及使用。")
            st.markdown("欢迎在:green[B站]或者:green[微信视频号]关注，了解更多精彩内容!")
            image = Image.open("./image/B.jpg")
            st.image(image, caption="", width=250)

    def my_info(self):
        st.write('\n')
        st.markdown('请在上面选项中选择【**注册**/**登陆**】开始使用')
        st.markdown("---")
        st.write("您好,欢迎关注我的**B站账号、微信视频号及公众号**👏")
        st.write("未来AI会像电脑一样普及，早用晚用不如现在就用！让我们一起探索AI的魅力吧🤔")
        st.write("️非常感谢您的关注与支持！🙏")
        st.write('\n')
        # 图片展示
        image1 = Image.open("./image/shipinhao.jpg")
        image2 = Image.open("./image/dingyuehao.jpg")
        image3 = Image.open("./image/wexin2.jpg")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(image1, caption="微信视频号", width=200)
        with col2:
            st.image(image2, caption="微信订阅号", width=200)
        with col3:
            st.image(image3, caption="微信交流", width=200)


    def main_interface(self,username):
        self.username = username
        st.write('#### 1.输入你的 OpenAI API [获取地址](https://platform.openai.com/account/api-keys) ')
        if not st.session_state['API']:
            API=st.text_input('OpenAI API-KEY',placeholder='在这里输入OpenAI API-KEY',type='password')
            st.session_state['API']=API
        else:
            st.success('OpenAI API-KEY已保存！')
            if st.button('清除API'):
                st.session_state['API'] = None
                st.success('OpenAI API-KEY已清除！请刷新')

        st.write('#### 2.创建数据库并提问')
        t1, t2 = st.tabs(['创建数据库', '提问'])
        with t1:
            Files=st.file_uploader('上传pdf/docx/txt/csv/md文件',
                                  type=['pdf','docx','txt','csv','md'],
                                  accept_multiple_files=True,
                                  disabled= not st.session_state['API']
                             )

            # if Files:
            #     newPath='./tmp/'+self.username+'/'
            #     os.makedirs(newPath,exist_ok=True)
            #     newFile=newPath+File.name
            #     with open(pathlib.Path(newFile),'wb') as f:
            #         f.write(File.read())
            # dbName = st.text_input('输入新建/更新数据库名称', disabled=not File)
            sub = st.button('提交',disabled= not Files)
            if sub:
                for File in Files:
                    newPath = './tmp/' + self.username + '/'
                    os.makedirs(newPath, exist_ok=True)
                    newFile = newPath + File.name
                    with open(pathlib.Path(newFile), 'wb') as f:
                        f.write(File.read())
                    db = CreateDB(self.username, newFile,st.session_state['API'])
                    db.store_qdrand()

        with t2:
            #读取数据库名称列表
            # st.write(st.session_state['API'])
            if not (st.session_state['API'] and st.session_state['API'].startswith('sk-')):
                st.error('请输入正确的 OpenAI API-KEY ！')
                st.stop()
            chain = get_chain(st.session_state['API'],self.username)
            question = st.text_input('提问：')
            if question:
                st.write(f'问：{question}')
                with get_openai_callback() as cb: #统计token
                    answer = chain.run(question)
                    st.write(f'答：{answer}')
                    st.success(f"消耗金额: ${cb.total_cost} (Tokens: {cb.total_tokens})")





