import os
import numpy as np

root_folder = os.path.join('/media/remus/datasets/Fall/Multiple_camera_fall/Multiple_camera_fall_dataset')
nested_folder = 'Annotation'
sync_file = '/media/remus/datasets/Fall/Multiple_camera_fall/sync.txt'

if __name__ == '__main__':

    sync = open(sync_file, "r")
    sync_line = sync.readlines()

    for scenario in sorted(os.listdir(root_folder)):
        number = int(scenario[5:]) - 1
        line = np.array(sync_line[number].strip().split(" ")[1:], dtype=np.int)
        line = line - np.ones(np.shape(line), dtype=np.int) * line[0]

        annot_folder = os.path.join(root_folder, scenario, nested_folder)
        annot_list = sorted(os.listdir(annot_folder))

        for j, annot_name in enumerate(annot_list):
            annot_path = os.path.join(annot_folder, annot_name)

            content = []
            with open(annot_path, "r") as f:
                content = f.readlines()

            # if len(content) > 3:
            content = [
                str(int(content[i]) + 2 * line[j]) + '\n' if i % 2 == 1 else str(
                    int(content[i]) + 2 * line[j]) + "\n" for i, _ in enumerate(content)]

            # content = [
            #     str(int(content[i]) + 64 ) + '\n' if i % 2 == 1 else str(
            #         int(content[i])) + "\n" for i, _ in enumerate(content)]

            # content1 = content[:2]
            # content2 = content[2:]
            # start = int(content1[1].strip())
            # end = int(content2[0].strip())
            # split = start + (end - start) / 2

            dim = len(content) - 1
            content[dim] = content[dim][:-1]

            with open(annot_path, "w") as f:
                f.writelines(content)
