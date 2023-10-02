import os
import time


def extract_timestamp(filename, prefix):
    """从文件名中提取时间戳"""
    return int(filename[len(prefix):].split('.')[0])  # 从文件名中去掉前缀和后缀，提取时间戳


def closest_timestamp(base_timestamp, timestamps_list):
    """找到与基准时间戳绝对值距离最小的时间戳"""
    return min(timestamps_list, key=lambda t: abs(base_timestamp - t))


# 指定两个文件夹的路径
yolo_folder = "D:\pluto\Desktop\colorimage"
depth_folder = "D:\pluto\Desktop\depthimage"

# 指定输出 TXT 文件的路径
output_txt = "D:\pluto\Desktop\\matched_images.txt"

# 已处理的文件列表
processed_depth_files = set()

while True:
    # 获取两个文件夹中的文件列表
    yolo_files = os.listdir(yolo_folder)
    depth_files = os.listdir(depth_folder)

    # 获取未处理的深度图文件
    new_depth_files = set(depth_files) - processed_depth_files

    if new_depth_files:
        with open(output_txt, "a") as txt_file:
            for depth_filename in new_depth_files:
                # 提取深度图的时间戳
                depth_timestamp = extract_timestamp(depth_filename, "depth")

                # 提取所有yolo图像的时间戳
                yolo_timestamps = [extract_timestamp(yolo_filename, "rgb") for yolo_filename in yolo_files]

                # 找到最接近的yolo图像的时间戳
                closest_yolo_timestamp = closest_timestamp(depth_timestamp, yolo_timestamps)

                # 构建文件路径
                yolo_file_path = os.path.join(yolo_folder, f"rgb{closest_yolo_timestamp}.png")
                depth_file_path = os.path.join(depth_folder, depth_filename)

                # 将文件路径写入到 TXT 文件中
                txt_file.write(f"{yolo_file_path}, {depth_file_path}\n")

                # 将文件添加到已处理文件列表中
                processed_depth_files.add(depth_filename)

        print(f"Processed {len(new_depth_files)} depth files.")

    # 每隔一段时间检查一次
    time.sleep(1)  # 你可以根据需要调整时间