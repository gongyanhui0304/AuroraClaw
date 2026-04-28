import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from base.config import *

load_dotenv()


def get_llm():
    llm = ChatOpenAI(
        # model="Qwen/Qwen3.5-35B-A3B",
        # model="Qwen/Qwen3.5-122B-A10B",
        model=BASE_LLM,
        base_url=MODEL_API_BASE_URL,
        api_key=OPENAI_API_KEY,
        temperature=0.1)
    return llm


def get_vlm():
    llm = ChatOpenAI(
        model=BASE_VLM,
        base_url=MODEL_API_BASE_URL,
        api_key=OPENAI_API_KEY,
        temperature=0.1)
    return llm


if __name__ == '__main__':
    llm = get_llm()
    res = llm.invoke("你是谁?")
    print(res)
