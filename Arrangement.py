import get_pic_from_video as gp
import directory_tree_traversal
import scor_onlie
import op_log
import ftp_op
import time
import configparser
import os.path


# 记录开始运行时间
start_time = time.strftime("%Y-%m-%d %X", time.localtime())
try:
    # 读取配置文件
    conf = configparser.ConfigParser()
    conf.read('arr_config.ini')
    # 要处理的本地目录
    local_path = conf.get("local", "local_path")
    # 筛选文件类型
    file_type = conf.get("local", "video_type")
    video_type = [x for x in file_type.split(', ')]
    # 截图存放位置
    save_picture_path = conf.get("local", "save_picture_path")
    # 成功上传ftp后，是否删除本地的文件
    del_localfile = conf.get("local", "del_file_afterupload")
    # nswf 接口地址
    scor_url = conf.get("nsfw", "nsfw_api")
    # 截图总数
    pic_cnt = int(conf.get("nsfw", "pic_cnt"))
    # 判断图片是否为 NSFW 的阈值
    threshold = conf.get("nsfw", "threshold")
    # ftp 信息
    ip = conf.get("ftp", "ip")
    port = conf.get("ftp", "port")
    username = conf.get("ftp", "username")
    pwd = conf.get("ftp", "pwd")
except Exception as write_err:
    op_log.log_to_file("读取配置文件失败. %s" % write_err)

try:
    # 要上传文件的ftp配置
    ftp_conn = ftp_op.ftpconnect(ip, int(port), username, pwd)
except:
    print("ftp 连接失败(%s:%s %s %s)" % (ip, port, username, pwd))
    op_log.log_to_file("ftp 连接失败(%s:%s %s %s)" % (ip, port, username, pwd))
    exit(1)

try:
    # 连接数据库，记录操作日志
    tb_name = 'video_arrange'
    db_name = 'arr_file.db3'
    con, cur = op_log.open_sqlite(db_name, tb_name)
    # 获取本地指定类型的文件列表
    videos = directory_tree_traversal.file_list(local_path, video_type)
    if not videos:
        print('get no file')
        log_txt = "start at %s , but get no file." % (start_time)
        op_log.log_to_file(log_txt)
        exit(0)
    cnt = 0
    for local_file in videos:
        cnt += 1
        print("-->:handling %s of %s " % (cnt, len(videos)))
        # 获取文件截图
        if not os.path.exists(save_picture_path):
            os.makedirs(save_picture_path)
        images = gp.get_frame(local_file, save_picture_path, pic_cnt)
        if not images:
            op_log.log_to_file("%s 获取文件截图失败" % local_file)
            continue
        # 记录超过阈值的个数
        scors_cnt = 0
        nsfw_flag = 0
        for ims in images:
            scors = scor_onlie.scor(scor_url, ims)
            if float(scors) > float(threshold):
                scors_cnt += 1
        success = 0
        if scors_cnt > 1:
            nsfw_flag = 1
            # 上传文件到ftp
            remote_file = os.path.split(local_file)[-1]
            upresult = ftp_op.uploadfile(ftp_conn, local_file, remote_file)
            if upresult is True:
                result_txt = local_file + '-- 上传ftp成功'
                success = 1
                if int(del_localfile) == 1:
                    os.remove(local_file)
                    op_log.log_to_file("删除文件:%s" % local_file)
            else:
                result_txt = local_file + '-- 上传ftp失败: ' + upresult
                success = 0
            # op_log.log_to_file(result_txt)
            txt = "%s| |upfile: %s| | %s" % (str(time.asctime()), local_file, result_txt)
            data = (os.path.split(local_file)[-1], local_file, int(nsfw_flag), result_txt, success, time.strftime("%Y-%m-%d %X", time.localtime()), '')
        else:
            result_txt = "不是NSFW文件，不上传"
            data = (os.path.split(local_file)[-1], local_file, int(nsfw_flag), result_txt, success, time.strftime("%Y-%m-%d %X", time.localtime()), '')
        op_log.insert_data(con, cur, tb_name, data)
        con.commit()
    end_time = time.strftime("%Y-%m-%d %X", time.localtime())
    log_txt = "complete | start at %s , finish at %s . handle %s files." % (start_time, end_time, cnt)
    op_log.log_to_file(log_txt)
except Exception as op_err:
    op_log.log_to_file("操作失败: %s" % op_err)
finally:
    ftp_conn.close()
    cur.close()
    con.close()
