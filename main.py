import streamlit as st

from predictor.inference import inference

import os
os.environ["OPENAI_API_KEY"] = ""

def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("main.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


st.markdown(f"""# GPT Interviewer""")
st.markdown("""\n""")
st.markdown(f"""#### 기업 평점 예측기""")
st.markdown("""\n""")
value = """직무: 기획/경영
고용 현황: 전직원
요약: "직원들간 평가로 업무역량을 판단하는 대표와 그 결과로 연봉협상을 통보식으로 진행함"
장점: 연차는 눈치 없이 쓸 수 있지만 정해진 가이드 또한 없다.
복지비 5만원이 제공되지만, 정작 개인이 원하는 복지비를 사용할 수 없다.
단점: 1. 한명 한명 직원의 평가를 다른 직원이 서로를 평가하는 시스템으로 업무역량을 판단하고
2. 그 결과를 토대로 연봉을 통보하며 제시한 연봉도 딱히 맘에 들지 않는다.
3. 좋은 사람도 있는 반면 정치질을 하는 사람 또한 있다.
경영진에게 바라는 점: 연봉협상 방식을 다르게 바꿔보는게 어떨까요
"""
review = st.text_area(label=" ", value=value, height=300, label_visibility="collapsed")
if st.button("기업 평점 예측"):
    score = str(inference(review))
    print(score)
    result = f"해당 기업의 평점은 {score}점 입니다."
    st.markdown(result)
st.markdown("""\n""")
if st.button("Start Interview!"):
    switch_page("interviewer")
st.markdown("""\n""")