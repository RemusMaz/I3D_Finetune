import os, sys
import argparse

#
# def get_video_list():
#     video_list = []
#     path_list = []
#     for cls_names in os.listdir(dir_frames):
#         cls_path = os.path.join(dir_frames, cls_names)
#         for video_ in os.listdir(cls_path):
#             video_list.append(video_)
#             path_list.append(os.path.join(cls_path, video_))
#     return video_list, path_list


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='ucf101', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/Fall_detection/annotated', type=str)
    parser.add_argument('--dir_frames', default='frames', type=str)
    parser.add_argument('--frames', default='../data/Fall_detection/frames.txt', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    data_root = os.path.join(args.data_root)

    folders = os.listdir(data_root)

    frames = open(args.frames, "w")

    for folder in folders:
        path_videos = os.path.join(data_root, folder, "Frames")
        path_annotations = os.path.join(data_root, folder, "Annotation_files")
        list_videos = os.listdir(path_videos)
        list_annotations = os.listdir(path_annotations)
        print(path_videos)

        for ann, video in zip(list_annotations, list_videos):

            anno_file = open(os.path.join(path_annotations, ann), "r")

            cls = anno_file.readline().strip()
            print(ann, video, cls)
            clas_id = 0 if int(cls) == 0 else 1

            path = os.path.join(path_videos, video)
            no = len(os.listdir(path))
            frames.write(video + " " + path + " " + str(no) + " " + str(clas_id) + "\n")

    # label_map = os.path.join(args.label_map)
    # dir_frames = os.path.join(data_root, args.dir_frames)
    # # specify the augments
    #
    # # get video list
    # video_list, path_list = get_video_list()
    #
    # frame_list = os.listdir(dir_frames)
    #
    # labels_file = open(label_map, "r")
    # labels = map(lambda x : x.strip(), labels_file.readlines())
    #
    # k = 1000
    # for video, path in zip(video_list, path_list):
    #     no = len(os.listdir(path))
    #     k = min(k, no)
    #     clas_id = labels.index(path.split("/")[7])
    #     frames.write(video + " " + path + " " + str(no) + " " + str(clas_id) + "\n")



