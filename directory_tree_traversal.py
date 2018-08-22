import os

def file_list(path=None, last_name=None):
    """
    遍历指定目录，返回文件完整路径的结果集
    :param path: 要遍历的路径
    :param last_name: 后缀名（默认全部文件）
    :return:
    """
    if not path:
        return None
    file_set = set()
    # file_list = []
    for fpath, dirs, fs in os.walk(path):
        # file_set = file_set | set(fs)
        # file_list.extend(fs)
        for fn in fs:
            # print('文件名：', fn)
            # print("完整路径名：",  os.path.join(fpath,fn))
            if not last_name:
                file_set.add(os.path.join(fpath,fn))
            elif type(last_name) is list:
                if fn.split('.')[-1] in last_name:
                    file_set.add(os.path.join(fpath,fn))
            else:
                return None
    return file_set