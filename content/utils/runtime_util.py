from langchain_core.runnables.config import var_child_runnable_config as vcrc
from base import config
import os

from utils.general_utils import loggers


# thread_id 通常存储在 configurable 字段中
def get_thread_id():
    config = vcrc.get()
    if config:  # 配置不为空
        configurable = config.get('configurable')
        if configurable:  # 配置不为空
            return configurable.get('thread_id', 'default')  # 返回 thread_id
    return "default"  # 返回默认值


def get_thread_dir():
    # os.path.normpath 是规划化路径的操作，重点就是'/'规划一下
    return os.path.normpath(os.path.join(config.WORK_SPACE, get_thread_id()))


def change_file_path(file_path):
    """
    将文件路径转换为当前线程对应的虚拟路径

    支持的输入格式：
    - 虚拟路径：\workspace\file.txt（直接返回）
    - Windows 绝对路径：E:\agent_workspace\file.txt
    - 相对路径：file.txt 或 ./file.txt

    输出格式：
    - 虚拟路径：\thread_id\file.txt 或 \workspace\file.txt
    """
    if not file_path or not isinstance(file_path, str):
        return file_path

    # 1. 如果已经是虚拟路径（以 \ 开头），直接返回
    #    例如：\skills\skill-creator\SKILL.md
    file_path = file_path.replace("/", "\\")

    if file_path.startswith('\\'):
        return file_path
    # 规范化文件路径，处理多余的分隔符、'.'和'..'等
    # 例如：/home//user/./docs/../file.txt -> /home/user/file.txt
    root_dir = os.path.normpath(get_thread_dir())
    path = os.path.normpath(file_path)  # 规范化路径
    if root_dir in path:
        rel = os.path.relpath(path, start=root_dir)
        return "\\" + rel.replace("/", "\\")
    if os.path.isabs(path):
        path = os.path.relpath(path, start=root_dir)
    virtual_path = os.path.normpath(path).replace("/", "\\")
    if not virtual_path.startswith("\\"):
        virtual_path = "\\" + virtual_path
    return virtual_path


def get_out_path(text):
    if not isinstance(text, str):
        return text
    # text = 'python /agent_files/aasdsada/a.py'
    # -> = 'python /a.py'
    # 先得到线程路径
    thread_dir = get_thread_dir()
    # 把text中存在的线程路径删除掉
    text = os.path.normpath(text)
    text = text.replace(thread_dir, '')
    return text


if __name__ == "__main__":
    # d = r'/aa/aa/a.py'
    # print(os.sep)
    # print(d)
    # print(os.path.normpath(d))
    print(change_file_path('user_upload/a.py'))
