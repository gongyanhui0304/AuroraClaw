import requests
import urllib3

# 关闭烦人的SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_image(image_url, save_path):
    # 下载图片（关闭SSL验证，解决阿里云OSS连接问题）
    response = requests.get(
        image_url,
        verify=False,  # 核心修复：关闭SSL证书验证
        timeout=30  # 防止卡死
    )

    # 确保请求成功
    response.raise_for_status()

    # 保存图片
    image_data = response.content
    with open(save_path, 'wb') as f:
        f.write(image_data)
