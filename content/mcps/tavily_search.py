import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from base import config as cfg
from dotenv import load_dotenv

load_dotenv()


def get_tavily_search_tools():
    '''
    联网搜索工具
    :return:检索结果
    '''
    client = MultiServerMCPClient(
        {
            "fetch": {
                "transport": "streamable_http",
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={cfg.TAVILY_SEARCH_KEY}"
            }
        },
    )
    return asyncio.run(client.get_tools())
