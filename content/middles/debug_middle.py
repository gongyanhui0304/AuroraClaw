from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import AgentState
import json

class DebugPrintMiddleware(AgentMiddleware):
    """
    调试中间件：打印 DeepAgent 中的 request 和 handler
    完全对齐你项目的 FileManagerMiddleware 格式
    """

    async def abefore_agent(self, state: AgentState, runtime):
        """Agent 执行前打印：state = request"""
        print("=" * 100)
        print("🔍 [DebugMiddleware] abefore_agent - request(state) 内容")
        print("=" * 100)

        try:
            print(json.dumps(state, indent=2, ensure_ascii=False, default=str))
        except:
            print(state)

        # 必须返回 None 或 dict，不修改逻辑
        return None

    async def awrap_model(self, request, handler):
        """
        这里就是你要的：
        request = 模型请求（prompt、messages、参数）
        handler = 模型执行器
        """
        print("\n" + "=" * 100)
        print("🤖 [DebugMiddleware] awrap_model - 打印 request + handler")
        print("=" * 100)

        # --------------------------
        # 打印你要的 request
        # --------------------------
        print("\n📥 请求内容 (request)：")
        print("类型：", type(request))
        try:
            print(json.dumps(request.__dict__, indent=2, ensure_ascii=False, default=str))
        except:
            print(request)

        # --------------------------
        # 打印你要的 handler
        # --------------------------
        print("\n⚙️ 执行器 (handler)：")
        print("类型：", type(handler))
        print(handler)

        # 执行原逻辑
        return await handler(request)

    async def awrap_tool_call(self, request, handler):
        """工具调用也打印 request + handler"""
        print("\n" + "=" * 100)
        print("🛠️ [DebugMiddleware] awrap_tool_call - 工具请求")
        print("=" * 100)

        print("\n📥 工具 request：")
        print(request)

        print("\n⚙️ 工具 handler：")
        print(handler)

        return await handler(request)