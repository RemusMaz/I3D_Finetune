import os, sys
import numpy as np
import cv2
from PIL import Image
from multiprocessing import Pool
import argparse
from IPython import embed  # to debug
import skvideo.io
import scipy.misc


def ToImg(raw_flow, bound):
    """
    this function scale the input pixels to 0-255 with bi-bound

    :param raw_flow: input raw pixel value (not in 0-255)
    :param bound: upper and lower bound (-bound, bound)
    :return: pixel value scale from 0 to 255
    """
    flow = raw_flow
    flow[flow > bound] = bound
    flow[flow < -bound] = -bound
    flow -= -bound
    flow *= (255 / float(2 * bound))
    return flow


def save_flows(flows, image, save_dir, num, video_name, bound):
    """
    To save the optical flow images and raw images
    :param flows: contains flow_x and flow_y
    :param image: raw image
    :param save_dir: save_dir name (always equal to the video id)
    :param num: the save id, which belongs one of the extracted frames
    :param bound: set the bi-bound to flow images
    :return: return 0
    """
    if flows is not None:

        # rescale to 0~255 with the bound setting
        flow_x = ToImg(flows[..., 0], bound)
        flow_y = ToImg(flows[..., 1], bound)
        if not os.path.exists(os.path.join(data_root, new_dir_flow, save_dir)):
            os.makedirs(os.path.join(data_root, new_dir_flow, save_dir))

    if not os.path.exists(os.path.join(data_root, new_dir_rgb, save_dir, video_name)):
        os.makedirs(os.path.join(data_root, new_dir_rgb, save_dir, video_name))

    # save the image
    save_img = os.path.join(data_root, new_dir_rgb, save_dir, video_name, 'img_{:05d}.jpg'.format(num))
    scipy.misc.imsave(save_img, image)

    # save the flows
    if flows is not None:
        save_x = os.path.join(data_root, new_dir_flow, save_dir, 'flow_x_{:05d}.jpg'.format(num))
        save_y = os.path.join(data_root, new_dir_flow, save_dir, 'flow_y_{:05d}.jpg'.format(num))
        flow_x_img = Image.fromarray(flow_x)
        flow_y_img = Image.fromarray(flow_y)
        scipy.misc.imsave(save_x, flow_x_img)
        scipy.misc.imsave(save_y, flow_y_img)
    return 0


def dense_flow(augs):
    """
    To extract dense_flow images
    :param augs:the detailed augments:
        video_name: the video name which is like: 'v_xxxxxxx',if different ,please have a modify.
        save_dir: the destination path's final direction name.
        step: num of frames between each two extracted frames
        bound: bi-bound parameter
    :return: no returns
    """
    video_name, save_dir, step, bound = augs
    folder = video_name.split('/')[0]
    video_name = video_name.split('/')[1]
    video_path = os.path.join(videos_root, folder, video_name)

    # provide two video-read methods: cv2.VideoCapture() and skvideo.io.vread(), both of which need ffmpeg support

    # videocapture=cv2.VideoCapture(video_path)
    # if not videocapture.isOpened():
    #     print 'Could not initialize capturing! ', video_name
    #     exit()
    try:
        videocapture = skvideo.io.vread(video_path)
    except:
        print '{} read error! '.format(video_name)
        return 0
    print video_name
    # if extract nothing, exit!
    if videocapture.sum() == 0:
        print 'Could not initialize capturing', video_name
        exit()
    len_frame = len(videocapture)
    frame_num = 0
    image, prev_image, gray, prev_gray = None, None, None, None
    num0 = 0
    while True:
        # frame=videocapture.read()
        if num0 >= len_frame:
            break
        frame = videocapture[num0]
        num0 += 1
        if frame_num == 0:
            image = np.zeros_like(frame)
            gray = np.zeros_like(frame)
            prev_gray = np.zeros_like(frame)
            prev_image = frame
            prev_gray = cv2.cvtColor(prev_image, cv2.COLOR_RGB2GRAY)
            frame_num += 1
            # to pass the out of stepped frames
            step_t = step
            while step_t > 1:
                # frame=videocapture.read()
                num0 += 1
                step_t -= 1
            continue

        image = frame
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        frame_0 = prev_gray
        frame_1 = gray
        ##default choose the tvl1 algorithm
        dtvl1 = cv2.createOptFlow_DualTVL1()

        # TODO comment this if you don't want to compute flow
        flowDTVL1 = None
        # flowDTVL1 = dtvl1.calc(frame_0, frame_1, None)
        if color is False:
            image = gray

        save_flows(flowDTVL1, image, save_dir, frame_num, video_name, bound)  # this is to save flows and img.
        prev_gray = gray
        prev_image = image

        frame_num += 1
        # to pass the out of stepped frames
        step_t = step
        while step_t > 1:
            # frame=videocapture.read()
            num0 += 1
            step_t -= 1


def get_video_list():
    video_list = []
    for cls_names in os.listdir(videos_root):
        cls_path = os.path.join(videos_root, cls_names)
        for video_ in os.listdir(cls_path):
            video_list.append(cls_names + "/" + video_)
    video_list.sort()
    return video_list, len(video_list)


def parse_args():
    parser = argparse.ArgumentParser(description="densely extract the video frames and optical flows")
    parser.add_argument('--dataset', default='TCL', type=str, help='set the dataset name, to find the data path')
    parser.add_argument('--data_root', default='/media/remus/datasets/TCL_Fall_Detection/avi', type=str)
    parser.add_argument('--new_dir_flow', default='flows', type=str)
    parser.add_argument('--new_dir_rgb', default='frames', type=str)
    parser.add_argument('--num_workers', default=2, type=int, help='num of workers to act multi-process')
    parser.add_argument('--step', default=2, type=int, help='gap frames')
    parser.add_argument('--bound', default=15, type=int, help='set the maximum of optical flow')
    parser.add_argument('--s_', default=0, type=int, help='start id')
    parser.add_argument('--e_', default=1251, type=int, help='end id')
    parser.add_argument('--mode', default='run', type=str, help='set \'run\' if debug done, otherwise, set debug')
    parser.add_argument('--color', default=False, type=bool, help='if frames ar rgb')

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    # example: if the data path not setted from args,just manually set them as belows.
    # dataset='ucf101'
    # data_root='/S2/MI/zqj/video_classification/data'
    # data_root=os.path.join(data_root,dataset)

    args = parse_args()
    data_root = os.path.join(args.data_root)
    videos_root = os.path.join(data_root, "avi")
    # specify the augments
    num_workers = args.num_workers
    step = args.step
    bound = args.bound
    color = args.color
    s_ = args.s_
    e_ = args.e_
    new_dir_flow = args.new_dir_flow
    new_dir_rgb = args.new_dir_rgb
    mode = args.mode
    # get video list
    video_list, len_videos = get_video_list()
    video_list = video_list[s_:e_]

    print 'find {} videos.'.format(len_videos)
    flows_dirs = [video.split('.')[0].split("/")[0] for video in video_list]
    print 'get videos list done! '

    pool = Pool(num_workers)
    if mode == 'run':
        pool.map(dense_flow, zip(video_list, flows_dirs, [step] * len(video_list), [bound] * len(video_list)))
    else:  # mode=='debug
        dense_flow((video_list[0], flows_dirs[0], step, bound))
