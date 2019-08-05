import os
import argparse

LEFT_EXTENSION = True
RIGHT_EXTENSION = False

def parse_split(file, print_file):
    lines = file.readlines()
    frame_interval = 64
    prediction = True

    for video_line in lines:
        path = video_line.strip()
        video = video_line.strip().split("/")
        video = "_".join(video[-3:])

        video_line = video_line.replace("Frames", "Annotation")
        path_annotations = video_line.strip() + ".txt"

        start_frame = 1
        end_frame = 1

        anno_file = open(path_annotations, "r")
        start_fall = int(anno_file.readline().strip())
        end_fall = int(anno_file.readline().strip())
        no_frames = len(os.listdir(path)) - 1

        if start_fall == 0:
            clas_id = 0
            end_frame = no_frames
        else:
            clas_id = 1

            start_frame = start_fall
            end_frame = end_fall

            extension = frame_interval - (end_fall - start_fall + 1)
            if extension <= 0:
                start_ext = int(max(1, start_fall - frame_interval / 4))
                end_ext = int(min(no_frames, end_fall + frame_interval / 2))
            else:
                # extension = min(int(frame_interval / 4), extension)
                start_ext = max(1, start_fall - extension)
                end_ext = min(no_frames, end_fall + extension)

            if prediction:
                start_frame = max(1, start_fall - frame_interval)
                end_frame = start_fall
            else:
                if LEFT_EXTENSION:
                    start_frame = start_ext

                if RIGHT_EXTENSION:
                    end_frame = end_ext

            if start_frame > frame_interval:
                line = video + "_left " + path + " " + str(1) + " " + str(start_frame - 1) + " " + str(0) + "\n"
                frames.write(line)
                print_file.write(line)

            if max(end_frame, end_ext) < no_frames - frame_interval:
                line = video + "_right " + path + " " + str(max(end_frame, end_ext) + 1) + " " + str(
                    no_frames) + " " + str(0) + "\n"
                frames.write(line)
                print_file.write(line)

        line = video + " " + path + " " + str(start_frame) + " " + str(end_frame) + " " + str(clas_id) + "\n"
        frames.write(line)
        print_file.write(line)


def parse_args():
    parser = argparse.ArgumentParser(description="Writing frame index.")
    parser.add_argument('--frames', default='../data/Fall_detection/rgb.txt', type=str)
    parser.add_argument('--train', default='../data/Fall_detection/train.txt', type=str)
    parser.add_argument('--val', default='../data/Fall_detection/val.txt', type=str)
    parser.add_argument('--split_train', default='../data/Fall_detection/split_train.txt', type=str)
    parser.add_argument('--split_val', default='../data/Fall_detection/split_val.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    split_train = open(args.split_train, "r")
    split_val = open(args.split_val, "r")

    frames = open(args.frames, "w")
    train = open(args.train, "w")
    val = open(args.val, "w")

    parse_split(split_train, train)
    parse_split(split_val, val)

    frames.close()
    train.close()
    val.close()
    split_train.close()
    split_val.close()
