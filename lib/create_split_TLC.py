import argparse
import os, sys
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='TLC', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/TCL_Fall_Detection/avi (1)/avi', type=str)
    parser.add_argument('--train', default='train.txt', type=str)
    parser.add_argument('--val', default='val.txt', type=str)
    args = parser.parse_args()
    return args


def get_video_list():
    train_file = open(train, "w")
    val_file = open(val, "w")
    for cls_names in os.listdir(data_root):
        cls_path = os.path.join(data_root, cls_names)
        videos_num = len(os.listdir(cls_path))

        split = np.random.choice(videos_num, videos_num, replace=False)
        train_len = int(videos_num * 0.8)

        aux = map(lambda x: cls_names + "/" + str(x + 1) + ".avi\n", split[:train_len])
        aux.sort()
        train_file.writelines(aux)

        aux = map(lambda x: cls_names + "/" + str(x + 1) + ".avi\n", split[train_len:])
        aux.sort()
        val_file.writelines(aux)

    train_file.close()
    val_file.close()


if __name__ == '__main__':
    args = parse_args()
    data_root = os.path.join(args.data_root)
    train = args.train
    val = args.val

    get_video_list()
