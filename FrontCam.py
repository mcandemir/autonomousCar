import cv2
import numpy as np
import json
from PIL import Image


class FrontCam:
    def __init__(self):
        """
        load the known signs
        """
        self.signs = None
        self.command = None
        with open('signs/signs_path.json', 'r') as f:
            self.signs = json.load(f)

        for sign, path in self.signs.items():
            self.signs[sign] = cv2.imread(path)

    def process(self, img):
        """
        finds the matched sign
        """

        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # for every known sign check if any exist
        for sign, sign_img in self.signs.items():

            # convert to gray
            sign_img = cv2.cvtColor(sign_img, cv2.COLOR_BGR2GRAY)

            # match templates
            res = cv2.matchTemplate(img_gray, sign_img, cv2.TM_CCOEFF_NORMED)

            # check if template (sign) matched
            threshold = 0.8
            if np.amax(res) > threshold:
                print("==========================")
                print(f'template found: {sign}')
                print("==========================")
                # # find the loc
                # w, h = sign_img.shape[::-1]
                # loc = np.where(res >= threshold)
                # for pt in zip(*loc[::-1]):
                #     cropped_sign = img[pt[1]: pt[1] + int(h/2), pt[0]: pt[0] + int(w/2)]

        cv2.imshow('front', img)

    # todo: function to act












