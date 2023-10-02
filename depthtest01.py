import cv2
import numpy as np
from openni import openni2, nite2


def visualize_depth(depth_image):
    # 归一化深度值
    depth_min = np.min(depth_image)
    depth_max = np.max(depth_image)
    normalized_depth = ((depth_image - depth_min) / (depth_max - depth_min) * 255).astype(np.uint8)

    # 应用伪彩色
    colored_depth = cv2.applyColorMap(normalized_depth, cv2.COLORMAP_JET)

    # 左右翻转图像
    flipped_depth = np.fliplr(colored_depth)

    return flipped_depth


# 初始化OpenNI
openni2.initialize()

# 打开Orbbec Astra设备
dev = openni2.Device.open_any()

# 创建深度流
depth_stream = dev.create_depth_stream()
depth_stream.start()

try:
    while True:
        # 读取深度帧
        frame = depth_stream.read_frame()

        # 将深度帧转换为NumPy数组
        frame_data = frame.get_buffer_as_uint16()
        depth_image = np.frombuffer(frame_data, dtype=np.uint16).reshape(frame.height, frame.width)

        # 可视化深度图像
        colored_depth = visualize_depth(depth_image)

        # 对彩色深度图像进行中值滤波
        filtered_depth = cv2.medianBlur(colored_depth, 5)

        # 使用OpenCV显示彩色深度图像
        cv2.imshow('Colored Depth Image', filtered_depth)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 停止深度流并关闭设备
    depth_stream.stop()
    dev.close()
    openni2.unload()

cv2.destroyAllWindows()