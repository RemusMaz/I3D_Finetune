import os, sys
import argparse
import random


def print_split(write_line):
    split = random.randint(1, 10)
    if split > 8:
        val.write(write_line)
    else:
        train.write(write_line)


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='ucf101', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/Fall/UR_Fall_Detection', type=str)
    parser.add_argument('--dir_frames', default='frames', type=str)
    parser.add_argument('--frames', default='../data/Fall_detection/rgb.txt', type=str)
    parser.add_argument('--train', default='../data/Fall_detection/train.txt', type=str)
    parser.add_argument('--val', default='../data/Fall_detection/val.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    data_root = os.path.join(args.data_root)

    folders = os.listdir(data_root)

    frames = open(args.frames, "a")
    train = open(args.train, "a")
    val = open(args.val, "a")

    for folder in folders:

        # if '04' in folder or '23' in folder:
        #     continue

        path_videos = os.path.join(data_root, folder, "Frames")
        path_annotations = os.path.join(data_root, folder, "Annotations")
        list_videos = sorted(os.listdir(path_videos))
        list_annotations = sorted(os.listdir(path_annotations))

        print(path_videos)

        frame_interval = 64

        for ann, video in zip(list_annotations, list_videos):
            start_frame = 1
            end_frame = 1

            anno_file = open(os.path.join(path_annotations, ann), "r")
            # lines = anno_file.readlines()

            start_fall = int(anno_file.readline().strip())
            end_fall = int(anno_file.readline().strip())
            print(ann, video, start_fall)

            path = os.path.join(path_videos, video)
            no_frames = len(os.listdir(path))

            if start_fall == 0:
                clas_id = 0
                end_frame = no_frames
            else:
                clas_id = 1

                extension = frame_interval - (end_fall - start_fall + 1)
                if extension <= 0:
                    start_ext = max(1, start_fall - frame_interval / 2)
                    end_ext = min(no_frames, end_fall + frame_interval / 2)
                else:
                    # extension = min(int((end_fall - start_fall) / 2), extension)
                    start_ext = max(1, start_fall - extension)
                    end_ext = min(no_frames, end_fall + extension)

                start_frame = start_ext
                end_frame = end_ext

                # start_frame = start_fall - frame_interval if start_fall >= frame_interval else 1
                # end_frame = end_fall + frame_interval if end_fall + frame_interval <= no_frames else no_frames

                if start_frame > frame_interval:
                    line = video + " " + path + " " + str(1) + " " + str(start_frame - 1) + " " + str(0) + "\n"
                    frames.write(line)
                    print_split(line)

                if end_frame < no_frames - frame_interval:
                    line = video + " " + path + " " + str(end_frame + 1) + " " + str(no_frames) + " " + str(0) + "\n"
                    frames.write(line)
                    print_split(line)

            line = video + " " + path + " " + str(start_frame) + " " + str(end_frame) + " " + str(clas_id) + "\n"
            frames.write(line)
            print_split(line)

    frames.close()
    train.close()
    val.close()
