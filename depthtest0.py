import cv2
import numpy as np
from openni import openni2, nite2

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

        # TODO: 对深度图像进行处理
        # ...

        # 使用OpenCV显示深度图像
        cv2.imshow('Depth Image', depth_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 停止深度流并关闭设备
    depth_stream.stop()
    dev.close()
    openni2.unload()

cv2.destroyAllWindows()