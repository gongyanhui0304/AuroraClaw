import os
from pathlib import Path

from dotenv import load_dotenv
import log
load_dotenv()

BASE_LLM=os.getenv("BASE_LLM")
MODEL_API_BASE_URL=os.getenv("MODEL_API_BASE_URL")
ROOT_DIR=os.path.normpath(os.getenv("ROOT_DIR"))

WORK_SPACE_RAW = os.getenv("WORK_SPACE", "./agent_workspace")
print(WORK_SPACE_RAW)
if os.path.isabs(WORK_SPACE_RAW):
    WORK_SPACE = os.path.normpath(WORK_SPACE_RAW)
else:
    WORK_SPACE = os.path.normpath(os.path.join(ROOT_DIR, WORK_SPACE_RAW))


OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LANGSMITH_API_KEY=os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")

LOG_DIR = Path(__file__).parent.parent/"log" # 当前脚本所在路径作为日志文件存储路径
NEED_CONSOLE_LOG = False

HOST_IP = os.getenv("HOST_IP")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_ENDPOINT = f"{HOST_IP}:{MINIO_PORT}"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET=os.getenv("MINIO_BUCKET")

USER_UPLOAD_DIR=os.getenv("USER_UPLOAD_DIR")
WAIT_RATE_LIMIT_RETRY=os.getenv("WAIT_RATE_LIMIT_RETRY")
WAIT_RATE_LIMIT_SEC=os.getenv("WAIT_RATE_LIMIT_SEC")

BASE_VLM = os.getenv("BASE_VLM")  # VLM 模型
IMAGE_MODEL = os.getenv("IMAGE_MODEL") # 基础生图模型
EDIT_IMAGE_MODEL = os.getenv("EDIT_IMAGE_MODEL") # 修改图像模型
SILICON_API_KEY = os.getenv("OPENAI_API_KEY") # 引入一下硅基流动的API_KEY因为调用生图模型无法利用langchain本身框架。
GENERATE_IMAGE_PATH =os.getenv("GENERATE_IMAGE_PATH")  # 生成图片保存目录

TAVILY_SEARCH_KEY = os.getenv("TAVILY_SEARCH_KEY")

USE_EXCEL =  True if os.getenv("USE_EXCEL") and os.getenv("USE_EXCEL") == 'true' else False
USE_PPT = True if os.getenv("USE_PPT") and os.getenv("USE_PPT") == 'true' else False

SKILL_DIR_PATH = 'skills'