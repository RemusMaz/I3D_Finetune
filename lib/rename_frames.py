import argparse
import os, sys
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--data_root', default='/media/remus/datasets/Fall/UR_Fall_Detection/UR_ADL/Frames',
                        type=str)
    parser.add_argument('--train', default='train.txt', type=str)
    parser.add_argument('--val', default='val.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    data_root = os.path.join(args.data_root)

    video_list = os.listdir(os.path.join("Frames", data_root))

    for video_name in video_list:
        txt_file = data_root + "/" + video_name + ".txt"
        os.system("touch " + txt_file)
        os.system("echo '0\\n0' >" + txt_file)
