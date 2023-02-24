import cv2
import os

width = 900
height = 600

listImg = os.listdir(f'background_img/old')
# imgList = []
for imgPath in listImg:
    img = cv2.imread(f'background_img/old/{imgPath}')
    # imgList.append(imgPath)
    img = cv2.resize(img, (width, height))
    cv2.imwrite(f'background_img/new/'+imgPath, img)
    print(*["Image", imgPath, f'is resized to {width} X {height}'])
