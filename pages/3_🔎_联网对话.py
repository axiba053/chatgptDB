import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from PIL import Image
from dotenv import load_dotenv
import os

curdir=os.path.dirname(__file__)
path=curdir.split('pages')[0]
load_dotenv(dotenv_path=path)

image = Image.open('./image/AIgirl.png')
st.set_page_config(page_title='三强的小屋', layout='wide', page_icon=image)
st.title("🔎 联网ChatGPT(测试)")

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



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "您好，我可以联网回答问题，请问你想知道什么？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="在这里输入问题"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.session_state['API'], streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
