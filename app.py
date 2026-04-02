import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path or ".env")



def load_meeting_notes(file_path: str) -> str:
    """读取会议记录文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_chain():
    """构建总结 chain"""

    # 1. 定义 Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional assistant that summarizes meeting notes clearly and concisely."),
        ("human", "Please summarize the following meeting notes:\n\n{meeting_notes}")
    ])

    # 2. 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-5.2",  # 你常用的模型
        temperature=0
    )

    # 3. 输出解析
    parser = StrOutputParser()

    # 4. 构建 chain
    chain = prompt | llm | parser

    return chain


OUTPUT_PATH = "meeting_summary.txt"


def main():
    # 文件路径（可以改成你的文件）
    file_path = "test.txt"

    # 读取文件
    meeting_notes = load_meeting_notes(file_path)

    # 构建 chain
    chain = build_chain()

    # 执行
    result = chain.invoke({
        "meeting_notes": meeting_notes
    })

    summary_text = "\n===== Meeting Summary =====\n\n" + result + "\n"
    print(summary_text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        out_file.write(summary_text)
    print(f"\nSaved summary to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
