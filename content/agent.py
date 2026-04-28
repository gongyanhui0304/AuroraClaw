import asyncio
from deepagents import create_deep_agent
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from content.middles import wait_rate_limit
from content.middles import file_manager_middle
from content.middles.debug_middle import DebugPrintMiddleware
from content.middles.file_manager_middle import FileManagerMiddleware
from content.middles.minio_middle import MinioMiddle
from content.middles.wait_rate_limit import wait_rate_limit
from content.others import mybackend
from conn.llms import get_llm
from content.mytools import globe_tools as gt, vlm_tool, gen_image
from content.mcps import tavily_search
from base import config as cfg
from content.middles.execute_middle import ExecuteMiddleware
if cfg.USE_EXCEL:
    from content.subagents import excel_agent
if cfg.USE_PPT:
    from content.subagents import ppt_agent
from content.middles import mySkillMiddle

class AllAgent():
    def __init__(self):
        prompt = f'''
         你是一个通用智能体，
         读取ppt,doc,xls,pdf等文件时优先使用get_file_content,
         做图文需求时,如无特殊说明，则先做md,然后转换为pdf,要特别注意图片引用路径。
         直到完成任务前，都不要停止。
         回答用户用中文。
         '''
        if cfg.USE_EXCEL:  # 新增的prompt
            prompt += '\n制作Excel的需求，优先使用子代理中的excel-agent。'
        if cfg.USE_PPT:
            prompt += '\n制作PPT的需求，优先使用子代理中的ppt-agent。注意：ppt-agent不是工具的名字，它是子智能体的名字，调工具应该是调用名为task的工具。'
        self.agent = create_deep_agent(
            model=get_llm(),
            tools=self._get_tools(),
            system_prompt=prompt,
            backend=mybackend.backend_factory,
            middleware=self._get_middles(),
            subagents=self._get_subagents(),
        )

    def _get_tools(self):
        tools = gt.get_tools()
        tools.append(vlm_tool.read_image)
        tools.append(gen_image.generate_image)
        if cfg.TAVILY_SEARCH_KEY:
            tools.extend(tavily_search.get_tavily_search_tools())

        return tools

    def _get_subagents(self):
        subagent = []
        if cfg.USE_EXCEL:
            subagent.append(excel_agent.get_agent())

        if cfg.USE_PPT:
            subagent.append(ppt_agent.get_agent())
        return subagent

    def _get_middles(self):
        middles = [FileManagerMiddleware(), wait_rate_limit, MinioMiddle(), ExecuteMiddleware()]
        middles.append(
            mySkillMiddle.MySkillsMiddleware(backend=mybackend.backend_factory, sources=[cfg.SKILL_DIR_PATH]))
        return middles

if __name__ == '__main__':
    agent = AllAgent().agent

