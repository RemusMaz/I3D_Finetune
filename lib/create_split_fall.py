import os
import argparse
import numpy as np


def print_split(cls_path):
    cls_path = np.array(cls_path)
    videos_num = len(cls_path)

    split = np.random.choice(videos_num, videos_num, replace=False)
    train_len = int(videos_num * 0.8)

    aux = split[:train_len]
    aux.sort()
    train.writelines(cls_path[aux])

    aux = split[train_len:]
    aux.sort()
    val.writelines(cls_path[aux])


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='ucf101', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/Fall/Multiple_camera_fall/Multiple_camera_fall_dataset', type=str)
    parser.add_argument('--dir_frames', default='frames', type=str)
    parser.add_argument('--frames', default='../data/Fall_detection/rgb.txt', type=str)
    parser.add_argument('--train', default='../data/Fall_detection/train.txt', type=str)
    parser.add_argument('--val', default='../data/Fall_detection/val.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    prediction = False

    args = parse_args()
    data_root = os.path.join(args.data_root)

    folders = os.listdir(data_root)

    frames = open(args.frames, "a")
    train = open(args.train, "a")
    val = open(args.val, "a")
    not_fall_list = []
    fall_list = []

    for folder in folders:
        if '04' in folder or '23' in folder:
            continue

        path_videos = os.path.join(data_root, folder, "Frames")
        path_annotations = os.path.join(data_root, folder, "Annotation")
        list_videos = sorted(os.listdir(path_videos))
        list_annotations = sorted(os.listdir(path_annotations))

        for ann, video in zip(list_annotations, list_videos):
            anno_file = open(os.path.join(path_annotations, ann), "r")

            start_fall = int(anno_file.readline().strip())
            end_fall = int(anno_file.readline().strip())
            print(ann, video, start_fall)

            path = os.path.join(path_videos, video)

            if start_fall == 0:
                not_fall_list.append(path + "\n")
            else:
                fall_list.append(path + "\n")

    print_split(not_fall_list)
    print_split(fall_list)

    frames.close()
    train.close()
    val.close()
