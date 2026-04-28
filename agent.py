import asyncio
from content.agent import AllAgent

# import os
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:6984"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:6984"
agent = AllAgent().agent

if __name__ == '__main__':
    asyncio.run(agent.run_agent())
