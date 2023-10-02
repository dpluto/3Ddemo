from openni import openni2
import numpy as np
import cv2

def mousecallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(y, x, dpt[y, x])

if __name__ == "__main__":
    openni2.initialize()
    dev = openni2.Device.open_any()
    print(dev.get_device_info())

    # 创建深度流
    depth_stream = dev.create_depth_stream()
    dev.set_image_registration_mode(True)
    depth_stream.start()

    # 创建RGB流  <-- 新增
    color_stream = dev.create_color_stream()  # <-- 新增
    color_stream.start()  # <-- 新增

    cv2.namedWindow('depth')
    cv2.setMouseCallback('depth', mousecallback)

    while True:
        # 读取深度帧
        frame = depth_stream.read_frame()
        dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        dpt2 *= 255
        dpt = dpt1 + dpt2
        dim_gray = cv2.convertScaleAbs(dpt, alpha=0.17)
        depth_colormap = cv2.applyColorMap(dim_gray, 2)
        cv2.imshow('depth', depth_colormap)

        # 读取RGB帧  <-- 修改
        color_frame = color_stream.read_frame()  # <-- 新增
        color_data = color_frame.get_buffer_as_triplet()  # <-- 新增
        color_image = np.frombuffer(color_data, dtype=np.uint8).reshape(480, 640, 3)  # <-- 新增
        cv2.imshow('color', color_image)  # <-- 修改

        key = cv2.waitKey(1)
        if int(key) == ord('q'):
            break

    depth_stream.stop()
    color_stream.stop()  # <-- 新增
    dev.close()