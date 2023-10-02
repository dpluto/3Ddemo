# new_script_parallel.py

from testdetect1 import detect, Options
from testdepth3 import depth_capture
from multiprocessing import Process

def run_detect():
    opt = Options()
    opt.weights = 'weights/yolov7.pt'
    opt.source = '0'
    opt.img_size = 640
    opt.conf_thres = 0.25
    opt.iou_thres = 0.45
    opt.device = ''
    opt.view_img = False
    opt.save_txt = False
    opt.save_conf = False
    opt.nosave = False
    opt.classes = None
    opt.agnostic_nms = False
    opt.augment = False
    opt.update = False
    opt.project = 'runs/detect'
    opt.name = 'exp'
    opt.exist_ok = False
    opt.no_trace = False

    opt.save_path = 'D:\\pluto\\Desktop\\colorimage'

    detect(opt)

def main():
    # 创建两个进程
    p1 = Process(target=run_detect)
    p2 = Process(target=depth_capture)

    # 启动两个进程
    p1.start()
    p2.start()

    # 等待两个进程完成
    p1.join()
    p2.join()

if __name__ == "__main__":
    main()