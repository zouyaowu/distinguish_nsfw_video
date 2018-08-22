try:
    from cv2 import VideoCapture, resize, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, imencode
except:
    print("导入 CV2 模块失败，请安装opecv_python模块，尝试运行此命令：pip install opencv_python")


def resize_pic(image, sz=(256, 256)):
    return resize(image, sz)
def get_frame(videoPath, svPath, pic_cnt=10):
    cap = VideoCapture(videoPath)
    """
    get 方法，可以有多个用途，后面跟的整数，依次表示下面的方法（从0开始）
    CV_CAP_PROP_POS_MSEC  视频文件的当前位置（以毫秒为单位）或视频捕获时间戳。
    CV_CAP_PROP_POS_FRAMES  接下来要解码/捕获的帧的基于0的索引。
    CV_CAP_PROP_POS_AVI_RATIO  视频文件的相对位置：0 - 电影的开始，1 - 电影的结尾。
    CV_CAP_PROP_FRAME_WIDTH  视频流中帧的宽度。
    CV_CAP_PROP_FRAME_HEIGHT  视频流中帧的高度。
    CV_CAP_PROP_FPS  帧速率。
    CV_CAP_PROP_FOURCC  编解码器的4字符代码。
    CV_CAP_PROP_FRAME_COUNT  视频文件中的帧数。
    CV_CAP_PROP_FORMAT  返回的Mat对象的格式  retrieve() 。
    CV_CAP_PROP_MODE  指示当前捕获模式的特定于后端的值。
    CV_CAP_PROP_BRIGHTNESS  图像的亮度（仅适用于相机）。
    CV_CAP_PROP_CONTRAST  图像对比度（仅适用于相机）。
    CV_CAP_PROP_SATURATION  图像的饱和度（仅适用于相机）。
    CV_CAP_PROP_HUE  图像的色调（仅适用于相机）。
    CV_CAP_PROP_GAIN  图像的增益（仅适用于相机）。
    CV_CAP_PROP_EXPOSURE  曝光（仅适用于相机）。
    CV_CAP_PROP_CONVERT_RGB  布尔标志，指示是否应将图像转换为RGB。
    CV_CAP_PROP_WHITE_BALANCE_U  白平衡设置的U值（注意：目前仅支持DC1394 v 2.x后端）
    CV_CAP_PROP_WHITE_BALANCE_V  白平衡设置的V值（注意：目前仅支持DC1394 v 2.x后端）
    CV_CAP_PROP_RECTIFICATION  立体摄像机的整流标志（注意：目前仅支持DC1394 v 2.x后端）
    CV_CAP_PROP_ISO_SPEED摄像机  的ISO速度（注意：目前仅支持DC1394 v 2.x后端）
    CV_CAP_PROP_BUFFERSIZE  存储在内部缓冲存储器中的帧数（注意：目前仅支持DC1394 v 2.x后端）    
    """
    try:
        # 获取视频的总帧数
        frame_cnt = cap.get(CAP_PROP_FRAME_COUNT)
        if int(pic_cnt) > int(frame_cnt):
            pic_cnt = int(frame_cnt)
        numFrame = 1
        # 总共截取多少张图片
        # 间隔多少帧截取一次
        betweenFrame = frame_cnt // pic_cnt
        # 截图列表
        images = []
        for i in range(pic_cnt):
            cap.set(CAP_PROP_POS_FRAMES, numFrame)
            flag, frame = cap.read()
            if flag:
                # cv2.imshow('frame', frmae)
                numFrame += betweenFrame
                # newPath = svPath + str(numFrame) + ".jpg"
                newPath = svPath + str(i) + ".jpg"
                frame = resize_pic(frame,(256, 256))
                imencode('.jpg', frame)[1].tofile(newPath)
                images.append(newPath)
            else:
                break
            # if cap.grab():
            #     flag, frame = cap.retrieve()
            #     if not flag:
            #         continue
            #     else:
            #         # cv2.imshow('video', frame)
            #         # numFrame += int(frame_cnt // pic_cnt) # 间隔
            #         numFrame += 1  # 间隔
            #         newPath = svPath + str(numFrame) + ".jpg"
            #         cv2.imencode('.jpg', frame)[1].tofile(newPath)
            # if cv2.waitKey(10) == 27:
            #     break
        return images
    except Exception as bug:
        print(bug)
        return None
    finally:
       cap.release()
