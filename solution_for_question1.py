# coding = utf-8
"""
@ Project: Wattman
@ Name: solution_for_question1
@ Author: kevin
@ Date: 2022/4/24 下午8:16
@ Email:caok15@sany.com.cn
"""

# import some standard libraries
import argparse
import json
import os

# import some third party libraries
import cv2


# coding here ======

def read_json(json_file):
    """
    Print out the "rectangle" field with the name "box_b" in the json file,
    and change the coordinate data structure from a dictionary to a list.
    :param json_file: path to json file
    :return: a list for bounding box coordinate.
                    [x1, y1, x2, y2]
            if parsing error returns None
    """
    # default return
    rect = None

    # read json file
    assert os.path.exists(json_file), 'json file: {} does not exist'.format(json_file)
    with open(json_file, 'r') as f:
        data = json.load(f)

    # get boxes info
    if data['boxes']:
        boxes_list = data['boxes']

        # search box_b
        for box in boxes_list:
            name, rectangle = box['name'], box['rectangle']

            if name == 'box_b':
                print('box_b rectangle: {}'.format(rectangle))
                # change the coordinate data structure from a dictionary to a list
                if rectangle['left_top'] and rectangle['right_bottom']:
                    rect = rectangle['left_top'] + rectangle['right_bottom']

    return rect


def patch_to_img(patch_img_file, background_img_file, box_b, mode='fill'):
    """
    Fill any image into the area specified by box_b of another image,
    and need to pass parameters to support two modes of "stretch fill" and "keep original proportion fill".
    :param mode: a string for patch resize mode.
                    'fill' -> "stretch fill" is default mode;
                    'orig' -> "keep original proportion fill".
    :param patch_img_file: image file path for patch
    :param background_img_file: image file path for background
    :param box_b: a list for bounding box.
                    [x1, y1, x2, y2]
    :return: None
    """
    # NoneType assert
    assert box_b is not None, "box_b is NoneType"

    # read images
    pt_img = cv2.imread(patch_img_file)
    bg_img = cv2.imread(background_img_file)
    assert pt_img is not None, "patch image is NoneType"
    assert bg_img is not None, "background image is NoneType"

    # get image info
    bg_h, bg_w, _ = bg_img.shape
    pt_h, pt_w, _ = pt_img.shape
    # get bounding box info
    x1, y1, x2, y2 = list(map(lambda x: int(round(x)), box_b))
    assert 0 <= x1 < x2 <= bg_w, "x position out of bounding or upside down"
    assert 0 <= y1 < y2 <= bg_h, "y position out of bounding or upside down"
    w, h = x2 - x1, y2 - y1

    # resize patch image and fill in background image
    assert mode in ['fill', 'orig'], "mode {} unsupported".format(mode)
    if mode == 'fill':
        # fill resize
        pt_img = cv2.resize(pt_img, (w, h))
        # plot patch on background img
        bg_img[y1:y2, x1:x2] = pt_img
    else:
        # keep original proportion fill
        ratio_w = w / pt_w
        ratio_h = h / pt_h
        ratio_min = min(ratio_w, ratio_h)
        pt_img = cv2.resize(pt_img, (0, 0), fx=ratio_min, fy=ratio_min)
        # get new size for patch image
        pt_h, pt_w, _ = pt_img.shape
        if pt_w >= pt_h:
            # padding in y dimension, keep patch center at box center
            padding = (h - pt_h) // 2
            # plot patch on background img
            bg_img[y1 + padding:y1 + padding + pt_h, x1:x2] = pt_img
        else:
            # padding in x dimension, keep patch center at box center
            padding = (w - pt_w) // 2
            # plot patch on background img
            bg_img[y1:y2, x1 + padding:x1 + padding + pt_w] = pt_img

    # show result
    # make a rectangle for clear show the bounding of box_b
    img2show = cv2.rectangle(bg_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    cv2.imshow('result', img2show)
    cv2.waitKey()

    # clear up
    cv2.destroyAllWindows()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=str, default='question1/boxes.json', help='path to json')
    parser.add_argument('--patch', type=str, default='question1/img_patch.jpg', help='path to patch image')
    parser.add_argument('--background', type=str, default='question1/img_background.jpg',
                        help='path to background image')
    parser.add_argument('--mode', type=str, default='fill', help='patch image resize mode. fill or orig')
    opt = parser.parse_args()
    return opt


# entrance =========
if __name__ == '__main__':
    args = parse_opt()
    box_position = read_json(args.json)
    patch_to_img(args.patch, args.background, box_position, args.mode)
