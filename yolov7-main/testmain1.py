from testdetect1 import detect, Options
from testdepth1 import depth_capture


def main():
    # 创建一个Options实例
    opt = Options()

    # 设置你需要的参数
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

    # 调用detect函数
    detect(opt)



if __name__ == "__main__":
    main()