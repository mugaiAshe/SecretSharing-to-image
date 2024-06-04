import cv2 as cv
import numpy as np
import random
from Crypto.Util.number import *

p = 257

#解填充，将二维图像转为一维数值并去除填充部分
def unpad(img):
    img = img.flatten()
    length = len(img)
    num = img[length-1]
    index = 1
    while True:
        if img[length-1-index] != num:
            break
        index += 1
    if index != num:
        index = 0
    return img[:length-index]

#恢复255、256
def addup(img):
    index = 0
    for x in range(len(img)):
        if img[len(img) - x - 1] == 255:
            img[len(img) - x - 1] = img[len(img) - index - 1] + img[len(img) - x - 1] - 1
            index += 1
    return img[:len(img) - index]

#用拉格朗日插值法计算秘密值
def lagrang(sons, keys):
    r, j = sons.shape
    sqare = np.zeros((r, r))
    for x in range(r):
        secret = np.zeros(r)
        bottom = 1
        flag = 1
        for y in range(r):
            if x == y:
                continue
            bottom *= keys[x] - keys[y]
            if flag:
                secret[0]= (keys[y]+1)*(-1)
                secret[1]= 1
                flag = 0
                continue
            temp = np.zeros(r)
            for z in range(r-1):
                temp[r-z-1] = secret[r-z-2] + secret[r-z-1]*(-1)*(keys[y]+1)
            temp[0] = secret[0]*(-1)*(keys[y]+1)
            secret = temp
        bottom = bottom % p
        secret = secret * inverse(bottom, p)
        sqare[x] = secret
    sqare = sqare.swapaxes(0,1)
    imgnum = np.mod(sqare @ sons, p)
    imgnum = imgnum[::-1]
    return imgnum

if __name__ == '__main__':
    # 解密过程，从n个阴影图像中随机选择r个
    r = int(input("输入r："))
    n = int(input("输入n："))
    user = random.sample(range(0, n), r)
    usrnum = np.array([])
    for keyid in user:
        son = cv.imread(str(keyid) + ".png", 0)
        # cv.imshow(str(keyid) + ".png", son)
        # cv.waitKey(0)
        sonnum = unpad(son)
        sonnum = sonnum.astype(np.int32)
        sonnum = addup(sonnum)
        print(sonnum)
        usrnum = np.append(usrnum, sonnum)
        print(keyid)
    usrnum = usrnum.reshape([r, -1])
    dekey = lagrang(usrnum, user)
    dekey = unpad(dekey)
    imglen = dekey[len(dekey) - 4:]
    height = int(imglen[0] * 256 + imglen[1])
    width = int(imglen[2] * 256 + imglen[3])
    dekey = dekey[:len(dekey) - 4]
    image = dekey.reshape(height, width, 3)
    print(image)
    cv.imwrite("recovered.png", image)