# langchain: https://python.langchain.com/
from typing import Literal
from dataclasses import dataclass

import nltk
import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA, ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import NLTKTextSplitter
from streamlit_lottie import st_lottie

from prompts.prompts import templates
from prompts.prompt_selector import prompt_sector


st.markdown("""\n""")
position = st.selectbox("지원 직무 선택", ["Data Analyst", "Software Engineer", "Marketing"])
resume = st.text_area("이력서를 써주세요.")

@dataclass
class Message:
    """Class for keeping track of interview history."""
    origin: Literal["human", "ai"]
    message: str

def save_vector(resume):
    """embeddings"""
    nltk.download('punkt')
    text_splitter = NLTKTextSplitter()
    texts = text_splitter.split_text(resume)

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    return docsearch

def initialize_session_state_resume():
    # convert resume to embeddings
    if 'docsearch' not in st.session_state:
        st.session_state.docserch = save_vector(resume)
    # retriever for resume screen
    if 'retriever' not in st.session_state:
        st.session_state.retriever = st.session_state.docserch.as_retriever(search_type="similarity")
    # prompt for retrieving information
    if 'chain_type_kwargs' not in st.session_state:
        st.session_state.chain_type_kwargs = prompt_sector(position, templates)
    # interview history
    if "resume_history" not in st.session_state:
        st.session_state.resume_history = []
        st.session_state.resume_history.append(Message(origin="ai", message="안녕하세요. 저는 AI 면접관입니다. 이력서와 경력에 대해 몇 가지 질문을 드리겠습니다. 인사나 자기소개로 시작하세요."))
    # token count
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    # memory buffer for resume screen
    if "resume_memory" not in st.session_state:
        st.session_state.resume_memory = ConversationBufferMemory(human_prefix = "지원자: ", ai_prefix = "면접관")
    # guideline for resume screen
    if "resume_guideline" not in st.session_state:
        llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,)

        st.session_state.resume_guideline = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type_kwargs=st.session_state.chain_type_kwargs, chain_type='stuff',
            retriever=st.session_state.retriever, memory = st.session_state.resume_memory).run("면접 가이드라인을 만들고 각 주제에 대해 2개의 질문만 준비하세요. 질문이 지식을 테스트하는지 확인하세요.")
    # llm chain for resume screen
    if "resume_screen" not in st.session_state:
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7, )

        eng_template = """I want you to act as an interviewer strictly following the guideline in the current conversation.
            
            Ask me questions and wait for my answers like a human. Do not write explanations.
            Candidate has no assess to the guideline.
            Only ask one question at a time. 
            Do ask follow-up questions if you think it's necessary.
            Do not ask the same question.
            Do not repeat the question.
            Candidate has no assess to the guideline.
            You name is GPTInterviewer.
            I want you to only reply as an interviewer.
            Do not write all the conversation at once.
            Candiate has no assess to the guideline.
            Make sure to translate the results into Korean and print them out
            
            Current Conversation:
            {history}
            
            Candidate: {input}
            AI: """ 

        PROMPT = PromptTemplate(
            input_variables=["history", "input"],
            template= """현재 대화에서 가이드라인을 철저히 지켜 면접관 역할을 해주셨으면 합니다.
            
            나에게 질문을 하고 사람처럼 대답을 기다리십시오. 설명을 쓰지 마십시오.
            지원자는 가이드라인에 대한 평가가 없습니다.
            한 번에 한 가지 질문만 하세요.
            필요하다고 생각되면 후속 질문을 하세요.
            같은 질문을 하지 마십시오.
            질문을 반복하지 마십시오.
            지원자는 가이드라인에 대한 평가가 없습니다.
            당신의 이름은 GPT 인터뷰어입니다.
            인터뷰 진행자로만 대답해 주셨으면 합니다.
            모든 대화를 한 번에 쓰지 마세요.
            지원자는 가이드라인에 대한 평가가 없습니다.
            
            현재 대화:
            {history}
            
            지원자: {input}
            면접관: """)
        st.session_state.resume_screen =  ConversationChain(prompt=PROMPT, llm = llm, memory = st.session_state.resume_memory)
    # llm chain for generating feedback
    if "resume_feedback" not in st.session_state:
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.5,)
        st.session_state.resume_feedback = ConversationChain(
            prompt=PromptTemplate(input_variables=["history","input"], template=templates.feedback_template),
            llm=llm,
            memory=st.session_state.resume_memory,
        )

def answer_call_back():
    with get_openai_callback() as cb:
        human_answer = st.session_state.answer
        input = human_answer
        st.session_state.resume_history.append(
            Message("human", input)
        )
        # OpenAI answer and save to history
        llm_answer = st.session_state.resume_screen.run(input)
        st.session_state.resume_history.append(
            Message("ai", llm_answer)
        )
        st.session_state.token_count += cb.total_tokens

if position and resume:
    # intialize session state
    initialize_session_state_resume()
    credit_card_placeholder = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        feedback = st.button("인터뷰 피드백 받기")
    with col2:
        guideline = st.button("면접 가이드라인을 알려주세요")
    chat_placeholder = st.container()
    answer_placeholder = st.container()
    audio = None
    # if submit email adress, get interview feedback imediately
    if guideline:
        st.markdown(st.session_state.resume_guideline)
    if feedback:
        evaluation = st.session_state.resume_feedback.run("인터뷰에 대한 평가를 부탁드립니다.")
        st.markdown(evaluation)
        st.download_button(label="인터뷰 피드백 다운로드", data=evaluation, file_name="interview_feedback.txt")
        st.stop()
    else:
        # with answer_placeholder:
        answer = st.chat_input("대답을 입력해 주세요.")
        if answer:
            st.session_state['answer'] = answer
            answer_call_back()

        with chat_placeholder:
            for answer in st.session_state.resume_history:
                if answer.origin == 'ai':
                    with st.chat_message("assistant"):
                        st.write(answer.message)
                else:
                    with st.chat_message("user"):
                        st.write(answer.message)

        credit_card_placeholder.caption(f"""
                        Progress: {int(len(st.session_state.resume_history) / 10 * 100)}% 완료.""")
                        # Progress: {int(len(st.session_state.resume_history) / 30 * 100)}% completed.""")

