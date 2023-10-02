from openni import openni2
import numpy as np
import cv2

# 初始化OpenNI
openni2.initialize()

# 打开Astra Pro设备
dev = openni2.Device.open_any()

# 创建深度流
depth_stream = dev.create_depth_stream()
depth_stream.start()

while True:
    # 读取深度帧
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    depth_image = np.frombuffer(frame_data, dtype=np.uint16).reshape(480, 640)  # 根据摄像头的分辨率调整

    # 将深度数据转换为可视化的图像
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # 判断真实物体和贴纸
    # 这里简化为使用深度阈值，实际应用可能需要更复杂的算法
    _, thresholded = cv2.threshold(depth_image, 1000, 65535, cv2.THRESH_BINARY_INV)  # 1000为示例阈值
    contours, _ = cv2.findContours(thresholded.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # 过滤小区域
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(depth_colormap, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Depth', depth_colormap)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

depth_stream.stop()
openni2.unload()
