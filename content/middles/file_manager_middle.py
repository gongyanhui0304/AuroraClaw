import asyncio
import os
import uuid
from uuid import uuid4
from os.path import exists
from typing import Callable, Awaitable, Any
import time
from langchain.agents.middleware.types import ResponseT, StateT
from langgraph.runtime import Runtime
from langgraph.typing import ContextT
from utils.doc_utils import zip_utils, base64_utils
from utils.doc_utils.os_utils import get_max_update_time
from utils.general_utils.loggers import logger
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse, ExtendedModelResponse
from langchain_core.messages import ToolMessage, AIMessage
from content.utils import runtime_util as ru
from utils.doc_utils import os_utils as ou
from conn.minio_conn import MinioConn
from base import config as cfg


class FileManagerState(AgentState):
    file_paths: set  # 存储文件路径的集合
    session_id: str
    upload_files: list


class FileManagerMiddleware(AgentMiddleware):
    state_schema = FileManagerState  # 状态赋值到类里

    def __init__(self):
        super().__init__()
        self.minio_conn = MinioConn()
        self.minio_conn.create_bucket_if_not_exists(cfg.MINIO_BUCKET)

    async def abefore_agent(self, state, runtime):
        state_dict = {}

        if ru.get_thread_id() != state.get('session_id', 'default'):  # 如果session_id和当前线程id不一致，则说明是切换会话窗口
            state_dict["session_id"] = ru.get_thread_id()
            session_path = ru.get_thread_dir()  # 获取当前会话的目录
            if os.path.exists(session_path):  # 如果这个目录存在
                file_paths = ou.get_all_files_path_in_dir(session_path)  # 获取当前目录下的所有文件路径
                state_dict["file_paths"] = file_paths
            else:
                state_dict["file_paths"] = set()

        upload_files = state.get('upload_files')
        if upload_files:
            session_path = ru.get_thread_dir()
            upload_dir = os.path.join(session_path, cfg.USER_UPLOAD_DIR)
            await asyncio.to_thread(os.makedirs, upload_dir, exist_ok=True)

            content = '用户上传了文件,路径如下:'
            for file in upload_files:
                base64_str = file.get('data')
                file_name = file.get('metadata').get('filename')
                # 调用一个函数，把base64_str转换成文件并保存，保存的路径由file_name与线程目录拼接(线程目录+user_upload+file_name)
                file_path = os.path.join(upload_dir, file_name)
                relative_file_path = os.path.join(cfg.USER_UPLOAD_DIR, file_name)
                content += f"\n{relative_file_path}"
                base64_utils.base64_to_file(base64_str, file_path)
            state_dict["messages"]: [ToolMessage(content=content, tool_call_id=uuid.uuid4().hex)]
            state_dict['upload_files'] = None
        return state_dict

    async def abefore_model(self, state: AgentState, runtime):
        session_path = ru.get_thread_dir()
        if os.path.exists(session_path):
            old_files = state.get('file_paths', set())
            current_files = ou.get_all_files_path_in_dir(session_path)
            if old_files != current_files:
                tree_str = ou.list_directory(session_path)
                return {"messages": [ToolMessage(content=tree_str, tool_call_id=uuid.uuid4().hex)],
                        'file_paths': current_files}
    async def awrap_tool_call(self, request, handler):

        # 调用具之前，把相对路径(假绝对路径)转换为真绝对路径
        filepath_fields = ['file_path', 'filepath', 'filename', 'image_path', 'reference_image_path']
        for field in filepath_fields:
            if field in request.tool_call['args']:
                request.tool_call['args'][field] = ru.change_file_path(request.tool_call['args'][field])

        try:
            result = await handler(request)  # 调用原本的工具函数
        except Exception as e:
            return ToolMessage(content=f"Error: {e}", tool_call_id=uuid4().hex, name=request.tool_call['name'])

        if isinstance(result, ToolMessage):
            result.content = ru.get_out_path(result.content)
        return result

