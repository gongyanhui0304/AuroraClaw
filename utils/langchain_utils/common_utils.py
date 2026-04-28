import os
from datetime import datetime
from pathlib import Path
from typing import Any


def save_graph_img(app: Any, file_name: str = None):
    """
    保存 LangGraph 结构图
    :param app: 编译后的 graph 对象 (app = workflow.compile())
    :param file_name: 文件名。如果不传，则使用 '年 月 日 _ 时 分 秒.png'
    """
    try:
        # 1. 确定保存的基础目录 (项目根目录下的 img 文件夹)
        # 获取当前文件所在目录的上一级，再找到 img 文件夹
        base_dir = Path(__file__).parent.parent.parent / "img"

        # 2. 如果没有提供文件名，生成时间戳文件名
        if not file_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{timestamp}.png"

        # 确保以 .png 结尾
        if not file_name.lower().endswith(".png"):
            file_name += ".png"

        # 3. 拼接完整路径并创建目录
        output_path = base_dir / file_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 4. 获取图片数据并写入
        # 注意: 某些环境下 draw_mermaid_png 需要安装 pygraphviz 或 pyppeteer
        img_data = app.get_graph().draw_mermaid_png()

        with open(output_path, "wb") as f:
            f.write(img_data)

        print(f"✅ 图结构已保存至: {output_path.absolute()}")

    except Exception as e:
        print(f"❌ 保存图片失败: {e}")
        print("提示: 确保已安装必要的绘图依赖，如 pygraphviz 或使用 app.get_graph().draw_png_pygraphviz()")
