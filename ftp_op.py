from ftplib import FTP
import os.path


def ftpconnect(host, port=21, uname=None, pwd=None):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(uname, pwd)
    return ftp

def uploadfile(ftp, localfile, remotefile):
    if not localfile or (not remotefile):
        return None
    buf_size = 1024
    try:
        with open(localfile, 'rb') as fp:
            ftp.storbinary('STOR ' + remotefile, fp, buf_size)
        # 通过对比本地文件大小与上传到ftp的文件大小，判断是否上传成功
        localfile_size = os.path.getsize(localfile)
        ftpfile_size = ftp.size(remotefile)
        if localfile_size != ftpfile_size:
            raise Exception ("上传文件校验失败")
    except Exception as bug:
        return bug
    return True

