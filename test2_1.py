# 导入必要的库
from openni import openni2
import numpy as np
import cv2

# 定义一个回调函数，当在窗口上双击鼠标左键时，打印深度信息
def mousecallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(y, x, dpt[y, x])

# 主程序开始
if __name__ == "__main__":
    # 初始化openni2
    openni2.initialize()
    # 打开任意连接的设备
    dev = openni2.Device.open_any()
    # 打印设备信息
    print(dev.get_device_info())
    # 创建深度流
    depth_stream = dev.create_depth_stream()
    # 设置图像注册模式（通常用于深度和RGB对齐）
    dev.set_image_registration_mode(True)
    # 开始深度流
    depth_stream.start()
    # 打开摄像头设备（这里是RGB摄像头）
    cap = cv2.VideoCapture(1)
    # 创建一个名为'depth'的窗口
    cv2.namedWindow('depth')
    # 设置鼠标回调函数（这里被注释掉了）
    # cv2.setMouseCallback('depth', mousecallback)
    # 设置捕获标志
    capture_flag = 0
    # 设置保存路径
    base_path = 'D:/RGBD_CAMERA/astra_chen_dataset/'
    # 设置图片计数器
    count = 1
    # 主循环
    while True:
        # 读取深度帧
        frame = depth_stream.read_frame()
        # 转换深度帧数据格式
        dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        dpt2 *= 255
        # 将两部分深度数据组合成一个16位的深度图像
        dpt = dpt1 + dpt2
        # 转换数据类型
        dpt = dpt.astype(np.uint16)
        # 将深度数据转换为灰度图像
        dim_gray = cv2.convertScaleAbs(dpt, alpha=0.17)
        # 对深度图像进行颜色映射
        depth_colormap = cv2.applyColorMap(dim_gray, 2)
        # 显示深度图像
        cv2.imshow('depth', depth_colormap)
        # 读取RGB摄像头的帧
        ret, frame = cap.read()
        # 显示RGB图像
        #cv2.imshow('color', frame)
        # 检查用户输入
        key = cv2.waitKey(30)
        if int(key) == ord('q'):
            break
        if int(key) == ord('r'):
            capture_flag = 1
        # 如果捕获标志被设置，保存深度和RGB图像
        if capture_flag == 1:
            name = str(count).zfill(8)
            cv2.imwrite(base_path + 'depth/' + name + ".png", dpt)
            cv2.imwrite(base_path + 'image/' + name + ".jpg", frame)
            count = count + 1
    # 停止深度流并关闭设备
    depth_stream.stop()
    dev.close()