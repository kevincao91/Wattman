# coding = utf-8
"""
@ Project: Wattman
@ Name: solution_for_question1
@ Author: kevin
@ Date: 2022/4/24 下午8:16
@ Email:caok15@sany.com.cn
"""

# import some standard libraries
import os

# import some third party libraries
import cv2


# coding here ======

def read_json():
    pass


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


# entrance =========
if __name__ == '__main__':
    patch_to_img('question1/img_patch.jpg', 'question1/img_background.jpg', [100, 100, 200, 200], 'fill')
