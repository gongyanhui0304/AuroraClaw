import shutil


# 打包文件夹成zip的方法
def zip_folder(folder_path, zip_path=None):
    if not zip_path:
        zip_path = folder_path
    return shutil.make_archive(zip_path, 'zip', folder_path)


if __name__ == '__main__':
    # zip_folder(r"E:\study\all_agent_study\all_agent_study\agent_workspace\80e279bc-6b4a-4627-a45c-30455407359c")
    folder_path = r"E:\study\all_agent_study\all_agent_study\agent_workspace"
    print(zip_folder(folder_path))
