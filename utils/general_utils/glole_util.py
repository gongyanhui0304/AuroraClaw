import sys


def get_platform():
    """
    获取当前操作系统平台
    :return:
    """

    platform = sys.platform
    if platform.startswith('win'):
        return 0  # Windows
    elif platform.startswith('linux') or platform.startswith('darwin'):
        return 1  # Linux/Mac
    else:
        return 2  # 其他平台


if __name__ == '__main__':
    print(get_platform())
