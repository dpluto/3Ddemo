import time
import cv2
import torch
import numpy as np
from pathlib import Path
from openni import openni2


DEPTH_THRESHOLD = 1000  # 您可以根据需要调整深度阈值


def detect(save_img=False):
    # 初始化深度流
    openni2.initialize()
    dev = openni2.Device.open_any()
    depth_stream = dev.create_depth_stream()
    depth_stream.start()

    # 初始化YOLOv7模型
    device = select_device('')
    model = attempt_load('weights/yolov7.pt', map_location=device)  # 加载模型
    stride = int(model.stride.max())
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    dataset = LoadStreams('0', img_size=640, stride=stride)  # 加载数据集

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device).float() / 255.0  # 归一化
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 进行物体检测
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)

        # 处理检测结果
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()

                # 获取深度信息
                for *xyxy, conf, cls in reversed(det):
                    x_center = int((xyxy[0] + xyxy[2]) / 2)
                    y_center = int((xyxy[1] + xyxy[3]) / 2)

                    frame = depth_stream.read_frame()
                    dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
                    dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
                    dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
                    dpt2 *= 255
                    dpt = dpt1 + dpt2

                    depth_value = dpt[y_center, x_center]

                    # 根据深度信息区分物体
                    if depth_value < DEPTH_THRESHOLD:
                        continue  # 如果深度值小于阈值，可能是贴纸，跳过此物体

                    # 画框并显示
                    label = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, im0s, label=label, color=colors[int(cls)], line_thickness=1)

        # 显示结果
        cv2.imshow('result', im0s)
        if cv2.waitKey(1) == ord('q'):  # 按q键退出
            break

    # 关闭深度流和设备
    depth_stream.stop()
    dev.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect()