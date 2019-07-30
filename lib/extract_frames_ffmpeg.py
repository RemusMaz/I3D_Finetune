import os
import cv2
import skvideo.io

if __name__ == '__main__':
    data_root = os.path.join('/media/remus/datasets/Fall/Fall_detection')

    for room in os.listdir(data_root):

        videos_root = os.path.join(data_root, room, "Videos")
        videos_list = os.listdir(videos_root)
        print(room)

        for video in videos_list:

            video_path = os.path.join(videos_root, video)
            video_name = video_path.split("/")[-1]
            frame_folder = os.path.join(data_root, room, "Frames", video_name.split(".")[0])

            if not os.path.exists(frame_folder):
                os.makedirs(frame_folder)

            videocapture = skvideo.io.vread(video_path)
            print(video, len(videocapture))

            for i, frame in enumerate(videocapture):
                filename = os.path.join(frame_folder, "frame_%04d.png" % int(i + 1))
                cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
