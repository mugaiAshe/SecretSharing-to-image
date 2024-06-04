import cv2 as cv
import numpy as np
import random
from Crypto.Util.number import *

p = 257

#填充函数，解决将一维数值转化为r高度的二维图像时除不整的问题，填充值为填充长度
def padimg(img, r):
    pad = len(img) % r
    if pad > 0:
        arr = np.ones(r - pad)
        arr = np.multiply(arr, r - pad)
        img = np.append(img, arr)
    img = img.reshape([r, -1])
    return img


if __name__ == '__main__':
    img = cv.imread('image.jpg')  # 直接以灰度图片读取
    cv.imshow("image.jpg", img)
    oldshape = np.array([int(img.shape[0]/256), img.shape[0]%256, int(img.shape[1]/256), img.shape[1]%256])
    print(img)
    cv.waitKey(0)
    img = img.flatten()
    img = np.append(img, oldshape) #将长度储存进数据尾部，因此只能读取255*256以内长度和宽度的图像

    r = int(input("输入r："))
    n = int(input("输入n："))
    secret = padimg(img, r)  #将秘密值分为r部分
    print("secret:")
    print(secret)
    sonlen = secret.shape[1]

    sons = np.ones((n, sonlen))  #计算n个阴影图像
    for keyid in range(n):
        sons[keyid] = secret[0]
        for index in range(r - 1):
            sons[keyid] = np.multiply(keyid+1, sons[keyid]) + secret[index + 1]
    sons = np.mod(sons, p)

    for keyid in range(n):
        son = sons[keyid]
        for x in range(sonlen):  #将255、256拆分为255+0、255+1，将1、2存入尾部
            if son[x] >= 255:
                pad = 1 + son[x] - 255
                son[x] = 255
                son = np.append(son, np.array(pad))
        print(son)
        print(keyid)
        son = padimg(son, int(pow(len(son), 0.5)))
        cv.imwrite(str(keyid) + ".png", son)
        # cv.imshow('son', son)
        # cv.waitKey(0)
