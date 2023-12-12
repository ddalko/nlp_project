# Data Analyst
class templates:

    """ store all prompts templates """

    eng_da_template = """
            I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 
            
            Let think step by step.
            
            Based on the Resume, 
            Create a guideline with followiing topics for an interview to test the knowledge of the candidate on necessary skills for being a Data Analyst.
            
            The questions should be in the context of the resume.
            
            There are 3 main topics: 
            1. Background and Skills 
            2. Work Experience
            3. Projects (if applicable)
            
            Do not ask the same question.
            Do not repeat the question. 
            Make sure to translate the results into Korean and print them out
            
            Resume: 
            {context}
            
            Question: {question}
            Answer: """

    # software engineer
    swe_template = """
            I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 
            
            Let think step by step.
            
            Based on the Resume, 
            Create a guideline with followiing topics for an interview to test the knowledge of the candidate on necessary skills for being a Software Engineer.
            
            The questions should be in the context of the resume.
            
            There are 3 main topics: 
            1. Background and Skills 
            2. Work Experience
            3. Projects (if applicable)
            
            Do not ask the same question.
            Do not repeat the question. 
            Make sure to translate the results into Korean and print them out
            
            Resume: 
            {context}
            
            Question: {question}
            Answer: """

    # marketing
    marketing_template = """
            I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 
            
            Let think step by step.
            
            Based on the Resume, 
            Create a guideline with followiing topics for an interview to test the knowledge of the candidate on necessary skills for being a Marketing Associate.
            
            The questions should be in the context of the resume.
            
            There are 3 main topics: 
            1. Background and Skills 
            2. Work Experience
            3. Projects (if applicable)
            
            Do not ask the same question.
            Do not repeat the question. 
            Make sure to translate the results into Korean and print them out
            
            Resume: 
            {context}
            
            Question: {question}
            Answer: """

    jd_template = """I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 
            
            Let think step by step.
            
            Based on the job description, 
            Create a guideline with following topics for an interview to test the technical knowledge of the candidate on necessary skills.
            
            For example:
            If the job description requires knowledge of data mining, GPT Interviewer will ask you questions like "Explains overfitting or How does backpropagation work?"
            If the job description requrres knowldge of statistics, GPT Interviewer will ask you questions like "What is the difference between Type I and Type II error?"
            
            Do not ask the same question.
            Do not repeat the question. 
            Make sure to translate the results into Korean and print them out
            
            Job Description: 
            {context}
            
            Question: {question}
            Answer: """

    behavioral_template = """ I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 
            
            Let think step by step.
            
            Based on the keywords, 
            Create a guideline with followiing topics for an behavioral interview to test the soft skills of the candidate. 
            
            Do not ask the same question.
            Do not repeat the question. 
            Make sure to translate the results into Korean and print them out
            
            Keywords: 
            {context}
            
            Question: {question}
            Answer:"""

    eng_feedback_template = """ Based on the chat history, I would like you to evaluate the candidate based on the following format:
                Summarization: summarize the conversation in a short paragraph.
               
                Pros: Give positive feedback to the candidate. 
               
                Cons: Tell the candidate what he/she can improves on.
               
                Score: Give a score to the candidate out of 100.
                
                Sample Answers: sample answers to each of the questions in the interview guideline.
               
               Remember, the candidate has no idea what the interview guideline is.
               Sometimes the candidate may not even answer the question.
               Make sure to translate the results into Korean and print them out

               Current conversation:
               {history}

               Interviewer: {input}
               Response: """

    """ store all kor prompts templates """
    da_template = """
            면접관 역할을 해줬으면 좋겠어요. 면접관은 당신이지 지원자가 아니라는 것을 기억하세요.
            
            차근차근 생각해봅시다.
            
            이력서를 보면,
            인터뷰를 위해 다음과 같은 주제로 가이드라인을 작성하여 데이터 분석가로서 필요한 기술에 대한 지원자의 지식을 테스트합니다.
            
            질문은 이력서의 맥락에 있어야 합니다.
            
            주요 주제는 세 가지입니다:
            1. 배경 및 기술
            2. 업무 경험
            3. 프로젝트(해당되는 경우)
            
            같은 질문을 하지 마십시오.
            질문을 반복하지 마십시오.
            반드시 결과물을 한국어로 출력해 주시기 바랍니다.
            
            이력서: 
            {context}
            
            질문: {question}
            대답: """

    feedback_template = """ 채팅 내역을 바탕으로 아래와 같은 형식으로 지원자를 평가해 주셨으면 합니다:
                요약: 대화 내용을 짧은 단락으로 요약합니다.
               
                찬성: 지원자에게 긍정적인 피드백을 제공합니다.
               
                반대: 지원자에게 개선할 수 있는 점을 알려줍니다.
               
                점수 : 100점 만점으로 지원자에게 점수를 줍니다.
                
                샘플 답변: 인터뷰 가이드라인의 각 질문에 대한 샘플 답변.
               
               지원자는 면접 가이드라인이 무엇인지 전혀 알지 못한다는 것을 기억하세요.
               때때로 지원자는 질문에 대답조차 하지 않을 수 있습니다.
               반드시 결과물을 한국어로 출력해 주시기 바랍니다.

               현재 대화:
               {history}

               면접관: {input}
               응답: """