import argparse
import os, sys
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--data_root', default='/media/remus/datasets/TCL_Fall_Detection/avi/frames', type=str)
    parser.add_argument('--train', default='train.txt', type=str)
    parser.add_argument('--val', default='val.txt', type=str)
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parse_args()
    data_root = os.path.join(args.data_root)
    train = args.train
    val = args.val

