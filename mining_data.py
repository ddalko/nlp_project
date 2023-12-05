import os
os.environ["OPENAI_API_KEY"] = ""

import json

from openai import OpenAI
client = OpenAI()

q_list = []
with open("question.txt", "r", encoding="utf-8") as f:
    q_list = [line.strip() for line in f.readlines()]

qna_list = []
for q in q_list:
    prompt = [
        {"role": "system", "content": "You are a interviewer."},
        {"role": "user", "content": q},
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    print(f"Question: {q}")
    print(completion.choices[0].message)
    prompt.append({"role": "assistant", "content": completion.choices[0].message.content})
    qna_list.append(prompt)

with open("interview_qna.jsonl", encoding="utf-8", mode="w+") as jfd:
    for i in qna_list:
        jfd.write(json.dumps(i) + "\n")
