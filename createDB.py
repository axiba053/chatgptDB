# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# 公众号/视频号/B站 ：三强的小屋
# Description：利用文本建立向量数据库
"""
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from dotenv import load_dotenv
import streamlit as st
import os

class CreateDB:
    def __init__(self,dbName,File,API,chunk_size=500,chunk_overlap=50):
        self.API=API
        self.dbName=dbName
        self.file=File
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        st.warning('待处理文件为：'+self.file.split("/")[-1])


    def split_file(self):
        loader = UnstructuredFileLoader(self.file)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        docs=text_splitter.split_documents(documents)
        str_num=len(documents[0].page_content)
        st.warning(f'文件中共有{str_num}个字符,拆分为{len(docs)}个子数据')
        cost= (str_num * 0.001)/0.85 * 0.0001 # 字数/0.85 Ktoken * 0.0001$/Ktoken
        cost2 = "< $0.01" if cost < 0.01 else ("$%.2f" % cost)
        st.success(f'消耗金额:  {cost2}')
        return docs

    def store_qdrand(self):
        docs=self.split_file()
        st.warning(f'向量数据库名称为：{self.dbName}')
        embeddings = OpenAIEmbeddings(openai_api_key=self.API)
        Qdrant.from_documents(
            docs, embeddings,
            url=os.getenv('QDRANT_HOST'),
            api_key=os.getenv('QDRANT_API_KEY'),
            collection_name=self.dbName,prefer_grpc=True,
        )
        st.success('已成功新建/更新数据库！请提问')

def main():
    load_dotenv()
    API=''
    File = 'data/test.docx'
    dbName='test'
    db=CreateDB(dbName,File,API)
    db.store_qdrand()

if __name__ == '__main__':
    main()

