import numpy as np
import cv2 

def cartoonize(save_path,path):
    image = cv2.imread(path)
    print(image.shape)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    edge = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

    iteration = 1
    filter = 10

    for i in range(iteration):
        image = cv2.pyrDown(image)
    print(image.shape)

    for i in range(filter):
        image = cv2.bilateralFilter(image, 9, 9, 7)
    print(image.shape)
    for i in range(iteration):
        image = cv2.pyrUp(image)
    
    
    
    (x,y, z)= image.shape
    edge = cv2.resize(edge, (y,x))
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
    kernel = np.ones((1, 1), np.uint8)
    edge = cv2.dilate(edge, kernel, iterations=1)

    image = cv2.bitwise_and(image, edge)
    cv2.imwrite(save_path, image)

