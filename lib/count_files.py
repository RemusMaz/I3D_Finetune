import os, sys
import argparse


def get_video_list():
    video_list = []
    path_list = []
    for cls_names in os.listdir(dir_frames):
        cls_path = os.path.join(dir_frames, cls_names)
        for video_ in os.listdir(cls_path):
            video_list.append(video_)
            path_list.append(os.path.join(cls_path, video_))
    return video_list, path_list


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='ucf101', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/TCL_Fall_Detection/avi', type=str)
    parser.add_argument('--dir_frames', default='frames', type=str)
    parser.add_argument('--label_map', default='../data/TCL/label_map.txt', type=str)
    parser.add_argument('--frames', default='../data/TCL/frames.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    data_root = os.path.join(args.data_root)
    label_map = os.path.join(args.label_map)
    dir_frames = os.path.join(data_root, args.dir_frames)
    # specify the augments

    # get video list
    video_list, path_list = get_video_list()

    frame_list = os.listdir(dir_frames)

    labels_file = open(label_map, "r")
    labels = map(lambda x : x.strip(), labels_file.readlines())

    frames = open(args.frames, "w")
    k = 1000
    for video, path in zip(video_list, path_list):
        no = len(os.listdir(path))
        k = min(k, no)
        clas_id = labels.index(path.split("/")[7])
        # frames.write(video + " " + path + " " + str(no) + " " + str(clas_id) + "\n")

    print(k)


