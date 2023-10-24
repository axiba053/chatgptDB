# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：
"""
import os
from langchain.callbacks import get_openai_callback
from PIL import Image
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import streamlit as st

curdir=os.path.dirname(__file__)
path=curdir.split('pages')[0]
load_dotenv(dotenv_path=path)

image = Image.open('./image/AIgirl.png')
st.set_page_config(page_title='三强的小屋', layout='wide', page_icon=image)
st.title('📺B站客服')
image1 = Image.open("./image/2233.png")
st.sidebar.image(image1, caption="", width=100)

info="大家好，我将[百度百科](https://baike.baidu.com/item/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9/8018053?fromtitle=bilibili&fromid=7056160&fromModule=lemma_search-box)" \
     "及[bilibili帮助页面](https://www.bilibili.com/blackboard/help.html)中B站相关内容上传数据库，搭建了一个B站AI客服系统。" \
     "欢迎大家提问～"

st.write(info)
st.markdown('---')

with st.sidebar:
    st.session_state['API'] = ''
    st.markdown(
        '输入**OpenAI-API** （[获取地址](https://platform.openai.com/account/api-keys)）或者**DB-API**（:red[点击下面免费获取]）')
    sub = st.button('免费获取DB-API')
    if sub:
        st.success('Bilibili扫码关注，回复口令【db-api】自动获取')
        image1 = Image.open("./image/B.jpg")
        st.image(image1, caption="", width=200)
    if not st.session_state['API']:
        API = st.text_input('API-KEY', placeholder='在这里输入API-KEY', type='password')
        st.session_state['API'] = API
    else:
        st.success('API-KEY已保存！')
        if st.button('清除API'):
            st.session_state['API'] = None
            st.success('API-KEY已清除！请刷新')
    #
    if st.session_state['API']:
        if st.session_state['API'].startswith('sk-'):
            pass
        elif st.session_state['API'].startswith('db-sqdxw'):
            st.session_state['API'] = os.getenv('OPENAI_API_KEY')
        else:
            st.warning('请输入OpenAI-API 或 DB-API ！')
            st.stop()
    else:
        st.info('请输入OpenAI-API 或 DB-API')


def get_chain(API,username):
    embeddings = OpenAIEmbeddings(openai_api_key=API)
    client = QdrantClient(
        url=os.getenv('QDRANT_HOST'),
        api_key=os.getenv('QDRANT_API_KEY'),
        prefer_grpc=True
    )
    vector_store = Qdrant(
        client=client,
        collection_name=username,
        embeddings=embeddings
    )
    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0,openai_api_key=API),
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True
    )
    return chain


def main_interface():
    st.session_state['API']=''
    username = 'bilibili'
    chain = get_chain(st.session_state['API'],username)
    question = st.text_input('问题：',placeholder='在这里输入问题')
    if question:
        st.write(f'问：{question}')
        with get_openai_callback() as cb: #统计token
            result = chain({"query": question})
            answer=result["result"]
            source=result["source_documents"][0].page_content
            # answer = chain.run(question)
            st.write(f'答：{answer}')
            with st.expander("来源"):
                st.markdown(source)
            # st.warning(f'来源：{source}')
            total_cost='%.2f' % cb.total_cost
            st.success(f"消耗金额: ${total_cost} (Tokens: {cb.total_tokens})")

main_interface()
