# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：根据提问查询数据库，将查询结果输入chatgpt输出答案
"""
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams,Distance
from qdrant_client.http.models import CollectionStatus
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

def create_collection(username):
    client = QdrantClient(
        url=os.getenv('QDRANT_HOST'),
        api_key=os.getenv('QDRANT_API_KEY'),timeout=30
    )
    #获取已有数据库名称
    collections_names=client.get_collections().collections
    collections_names_list=[col.name for col in collections_names]
    if username in collections_names_list:
        st.success(f'使用已有数据库{username}')
    else:
        client.recreate_collection(
            collection_name=username,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        collection_info = client.get_collection(collection_name=username)
        if collection_info.status == CollectionStatus.GREEN:
            # print('成功')
            st.success(f'新建数据库：{username}')
    st.success('注册成功！请从上面「界面」处选择登录')

# create_collection('你好')

def get_chain(API,username):
    embeddings = OpenAIEmbeddings(openai_api_key=API,embedding_ctx_length=10000)
    client = QdrantClient(
        url=os.getenv('QDRANT_HOST'),
        api_key=os.getenv('QDRANT_API_KEY'),
        prefer_grpc=True
    )
    #获取collections列表
    # dbNames=client.get_collections().collections
    # dbNames_tuple=tuple([col.name for col in dbNames])
    # DbName = st.selectbox('选择数据库：', dbNames_tuple)
    vector_store = Qdrant(
        client=client,
        collection_name=username,
        embeddings=embeddings
    )
    # 定制提示词
    prompt_template = """请扮演B站(bilibili)的AI客服，你可以回答bilibili相关问题。结合下面背景信息来回答最后的问题。如果内容与问题无关,请用礼貌友好的语气回复。

        {context}

        Question: {question}
        Answer:
        """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0,openai_api_key=API,max_tokens=1000),
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    return chain


# def main():
#     API=''
#     question=''
#     chain = get_chain(API)
#     answer = chain.run(question)

# if __name__ == '__main__':
#     main()
