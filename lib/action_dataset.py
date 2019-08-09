import time

import numpy as np
from lib.video_3d import Video_3D


class Action_Dataset:
    def __init__(self, name, mode, video_info):
        self.name = name
        self.mode = mode
        self.videos = [Video_3D(x, self.mode) for x in video_info]
        # the size is maybe the number of videos
        self.size = len(self.videos)
        self.epoch_completed = 0
        self.index_in_epoch = 0
        self.perm = np.arange(self.size)

        # Edited by Alex Hu
        np.random.shuffle(self.perm)

    def next_batch(self, batch_size, frame_num, shuffle=True, data_augment=True, random_start=False):
        # used for counting the number of epoches,
        # end is current number of the total processed videos
        # index_in_epoch is the index of this epoch
        start = self.index_in_epoch
        end = start + batch_size
        self.index_in_epoch = end % self.size
        batch = []
        label = []

        # start_time = time.time()

        if end >= self.size:
            self.epoch_completed += 1
            for i in range(start, self.size):
                # construct batch from start to the size
                batch.append(
                    self.videos[self.perm[i]].get_frames(frame_num, data_augment=data_augment,
                                                         random_start=random_start))
                label.append(self.videos[self.perm[i]].label)
            if shuffle:
                np.random.shuffle(self.perm)
            for i in range(0, self.index_in_epoch):
                batch.append(
                    self.videos[self.perm[i]].get_frames(frame_num, data_augment=data_augment,
                                                         random_start=random_start))
                label.append(self.videos[self.perm[i]].label)
        else:

            for i in range(start, end):
                print(self.videos[self.perm[i]].name)

                batch.append(
                    self.videos[self.perm[i]].get_frames(frame_num, data_augment=data_augment,
                                                         random_start=random_start))
                label.append(self.videos[self.perm[i]].label)

        # duration = time.time() - start_time
        # print("Time: ", duration)

        return np.stack(batch), np.stack(label)


def split_data(data_info, test_split):
    f1 = open(data_info)
    f2 = open(test_split)
    test = list()
    train_info = list()
    test_info = list()
    # extract the specific video name,and plus a document name behind,the result is such v_ApplyEyeMakeup_g01_c01
    for line in f2.readlines():
        test.append(line.strip())

    # if rgb's doc name is in testlist,then append in test_info,if not, append in train
    # for example, info is
    # v_ApplyEyeMakeup_g01_c01,/data4/zhouhao/dataset/ucf101/jpegs_256/v_ApplyEyeMakeup_g01_c01,165,0
    for line in f1.readlines():
        info = line.strip()

        if info in test:
            test_info.append(line.strip().split(" "))
        else:
            train_info.append(line.strip().split(" "))
    f1.close()
    f2.close()
    return train_info, test_info
