#!/usr/bin/env python3


import mss
import numpy as np
import cv2

for _ in range(100):
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1560, "height": 800}
        img_array = np.array(sct.grab(monitor))
        cv2.imshow("poo", img_array)
        cv2.waitKey()
        cv2.destroyAllWindows()