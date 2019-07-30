import os
import cv2
from multiprocessing import Process, Queue

root_folder = os.path.join('/media/remus/datasets/Fall/Fall_detection')


class Worker(Process):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue

    def run(self):
        print('Worker started')

        for annot_path in iter(self.queue.get, None):
            image = cv2.imread(annot_path)
            image = cv2.resize(image, (224, 224))
            cv2.imwrite(annot_path, image)


if __name__ == '__main__':
    request_queue = Queue()
    for i in range(4):
        Worker(request_queue).start()

    for folder in sorted(os.listdir(root_folder)):
        print(folder)

        annot_folder = os.path.join(root_folder, folder)
        annot_list = os.listdir(annot_folder)

        for scenario in sorted(os.listdir(os.path.join(root_folder, folder, "Frames"))):
            annot_folder = os.path.join(os.path.join(root_folder, folder, "Frames"), scenario)
            annot_list = os.listdir(annot_folder)

            for annot_name in annot_list:
                annot_path = os.path.join(annot_folder, annot_name)

                request_queue.put(annot_path)

                # print(annot_path)
                # new_path = os.path.join(annot_folder, "frame_{:04d}".format(int(annot_name.split('-')[-1].split('.')[0])) + ".png")
                # print(new_path)
                # print()

                # os.rename(annot_path, new_path)

    for i in range(4):
        request_queue.put(None)