try:
    import requests
except:
    print("导入 requests 模块失败，请安装(pip install request)")


def scor(url=None, file=None):
    # url = 'http://193.112.248.98/upload'
    # file_path = 'g:\\tmp\\image_test'
    #
    # for fpath, dirs, fs in os.walk(file_path):
    #     for fn in fs:
    #         filename = fpath + "\\" + fn
    #         image_file = resize_image(filename)
    #         files = {'filename': ('pic.jpg', open(image_file, 'rb'), 'image/jpeg')}
    #         r = requests.post(url, files=files)
    #         print(fn, ":", r.text)
    if not url or (not file):
        return None
    files = {'filename': ('pic.jpg', open(file, 'rb'), 'image/jpeg')}
    r = requests.post(url, files=files)
    return r.text

