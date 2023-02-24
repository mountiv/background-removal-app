import os
import cv2
import numpy as np
import mediapipe as mp

mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
cap = cv2.VideoCapture(0)

width = 900
height = 600
bg_img = cv2.imread(f'background_img/new/bg1.jpg')

while True:
    frame = cv2.imread("./human_img/1.jpg")
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # get the result
    results = selfie_segmentation.process(RGB)
    # extract segmented mask
    mask = results.segmentation_mask
    condition = np.stack((mask,) * 3, axis=-1) > 0.5
    # bg_img = cv2.resize(bg_img, (width, height))
    output_image = np.where(condition, frame, bg_img)
    # show outputs
    cv2.imshow("Output", output_image)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break