from langchain.messages import AIMessageChunk
from utils.general_utils.loggers import logger


# 流式打印日志
def stream_log(agent, input):
    res = agent.stream({"messages": [{'role': 'user', 'content': input}]})
    for i in res:
        logger.info(i[1])


# 流式打印token
def stream_token(agent, input):
    res = agent.stream({"messages": [{'role': 'user', 'content': input}]}, stream_mode=['messages'])
    for i in res:
        token = i[1][0].content
        if token.strip():
            if type(i[1][0]) == AIMessageChunk:  # 2. 过滤掉toolmessage (通过判断它的数据类型是否是AIMessageChunk)
                print(token, end="")


# 流式打印日志与token
def stream_both(agent, input):
    # 需求
    # 传入智能体和用户的输入，流式打印updates的日志与流式打印token,并且token要提出来打印
    res = agent.stream({"messages": [{'role': 'user', 'content': input}]}, stream_mode=['updates', 'messages'])
    for i in res:
        if i[0] == 'updates':  # 通过判断元组中的第一个是否是updates，来判断是否是打印日志
            logger.info(i[1])
        else:
            # 1. 过滤掉空token
            token = i[1][0].content
            if token.strip():
                if type(i[1][0]) == AIMessageChunk:  # 2. 过滤掉toolmessage (通过判断它的数据类型是否是AIMessageChunk)
                    print(token, end="")


class Memory:
    def __init__(self):
        self.messages = ''

    def stream_both_with_memory(self, agent, input):
        # 需求
        # 传入智能体和用户的输入，流式打印updates的日志与流式打印token,并且token要提出来打印
        self.messages = "user:" + self.messages + input + "AI:"
        res = agent.stream({"messages": [{'role': 'user', 'content': self.messages}]},
                           stream_mode=['updates', 'messages'])
        for i in res:
            if i[0] == 'updates':  # 通过判断元组中的第一个是否是updates，来判断是否是打印日志
                logger.info(i[1])
            else:
                # 1. 过滤掉空token
                token = i[1][0].content
                if token.strip():
                    if type(i[1][0]) == AIMessageChunk:  # 2. 过滤掉toolmessage (通过判断它的数据类型是否是AIMessageChunk)
                        print(token, end="")
                        self.messages = self.messages + token
