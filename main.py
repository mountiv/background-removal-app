import os
import cv2
import numpy as np
import mediapipe as mp
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
cap = cv2.VideoCapture(0)
while True:
    frame = cv2.imread("./human_img/1.jpg")
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # get the result
    results = selfie_segmentation.process(RGB)
    # extract segmented mask
    mask = results.segmentation_mask
    # show outputs
    cv2.imshow("mask", mask)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break