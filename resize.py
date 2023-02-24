import cv2
import os

listImg = os.listdir(f'background_img/old')
# imgList = []
for imgPath in listImg:
    img = cv2.imread(f'background_img/old/{imgPath}')
    # imgList.append(imgPath)
    img = cv2.resize(img, (900, 500))
    cv2.imwrite(f'background_img/new/'+imgPath, img)
    print(*["Image", imgPath, "is resized to 900 X 500"])

