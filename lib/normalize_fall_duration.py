import os

root_folder = os.path.join('/media/andrettin/27d6e7a9-9747-4a23-b788-27ac273d328b/ACTION_RECOGNITION/datasets/Multiple_camera_fall_dataset/dataset')
nested_folder = 'Annotation'

if __name__ == '__main__':
    for scenario in sorted(os.listdir(root_folder)):
        annot_folder = os.path.join(root_folder, scenario, nested_folder)
        annot_list = os.listdir(annot_folder)

        for annot_name in annot_list:
            annot_path = os.path.join(annot_folder, annot_name)

            content = []
            with open(annot_path, "r") as f:
                content = f.readlines()

            content = [str(int(content[i]) - 64) + '\n' if i % 2 == 1 else content[i] for i, _ in enumerate(content)]
            dim = len(content) - 1
            content[dim] = content[dim][:-1]

            with open(annot_path, "w") as f:
                f.writelines(content)

