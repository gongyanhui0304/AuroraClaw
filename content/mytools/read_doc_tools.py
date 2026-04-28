from utils.doc_utils import markitdown_utils


def get_file_content(file_path):
    '''
    读取文档内容
    :param file_path:文档路径
    :return: 文档内容
    '''
    return markitdown_utils.get_file_content(file_path)
