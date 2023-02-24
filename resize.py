import cv2
import os

# for root, subdirs, files in os.walk('E:/2023-02-24/Meetn_Camera_App/background_img'):
#     for f in files:
#         if f.endswith('jpg'):
#             # print(f)
#             img = cv2.imread('E:/2023-02-24/Meetn_Camera_App/background_img/' + f)
#             img = cv2.resize(img, (640, 480))
#             cv2.imwrite('E:/2023-02-24/Meetn_Camera_App/background_img/new/'+f, img)
#             print(*["Image", f, "is resized to 640 X 480"])

listImg = os.listdir(f'background_img/old')
# imgList = []
for imgPath in listImg:
    img = cv2.imread(f'background_img/old/{imgPath}')
    # imgList.append(imgPath)
    img = cv2.resize(img, (900, 500))
    cv2.imwrite(f'background_img/new/'+imgPath, img)
    print(*["Image", imgPath, "is resized to 800 X 600"])

