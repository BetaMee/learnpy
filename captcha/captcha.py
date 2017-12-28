
#!/usr/bin/env python
# encoding: utf-8
import os
import uuid
import cv2
import numpy as np


def get_row_rect(image):
    height,width = image.shape[:2]
    h = [0] * height
    for y in range(height):
        for x in range(width):
            s = image[y,x] #max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 0:
                h[y] += 1
    in_line = False
    start_line = 0
    ####
    blank_distance = 1
    ####
    row_rect = (0,0)
    for i in range(len(h)):
        if not in_line and h[i]>=blank_distance:
            in_line = True
            start_line = i
        elif in_line and h[i]<blank_distance:
            row_rect = (start_line,i)
            break

    return row_rect

def get_col_rect(image):
    height,width = image.shape[:2]
    h = [0] * width # 生成一个长度为width的数组，这里为66
    for x in range(width):
        for y in range(height):
            s = image[y,x] #max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 0:
                h[x] += 1
    col_rect = []
    in_line = False
    start_line = 0
    #####
    blank_distance = 1
    ####
    for i in range(len(h)):
        if not in_line and h[i]>=blank_distance:
            in_line = True
            start_line = i
        elif in_line and h[i]<blank_distance:
            rect = (start_line,i)
            col_rect.append(rect)
            in_line = False
            start_line = 0

    return col_rect

def get_block_image(image,col_rect):
    col_image = image[0:image.shape[0],col_rect[0]:col_rect[1]]
    row_rect = get_row_rect(col_image)
    #print row_rect
    if row_rect[1] != 0:
        block_image = image[row_rect[0]:row_rect[1],col_rect[0]:col_rect[1]]
    else:
        block_image = None
    return  block_image

# 提取相应颜色，并保存
def extractColor(filename):
    image = cv2.imread(filename)
    # 提取颜色参数
    color = [
        ([25, 25, 25], [100, 100, 100]) #颜色参数~注意：数值按[b,g,r]排布
    ]
    #如果color中定义了几种颜色区间，都可以分割出来 
    for (lower, upper) in color:
        # 创建NumPy数组
        lower = np.array(lower, dtype = "uint8")#颜色下限
        upper = np.array(upper, dtype = "uint8")#颜色上限
        # 根据阈值找到对应颜色
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)
        # 输出
        extractImg_filename = 'extractImgs/'+str(uuid.uuid4())+'.png'
        cv2.imwrite(extractImg_filename, output)

        return extractImg_filename

# 清除背景
def clean_bg(filename):
    image = cv2.imread(filename, 0) # 读取文件
    new_image = np.zeros(image.shape, np.uint8)
    height,width= image.shape
    # 将旧图的数据赋值到新图
    for i in range(height):
        for j in range(width):
            new_image[i,j] = image[i,j] #max(image[i,j][0],image[i,j][1],image[i,j][2])
    # 阈值处理
    ret,new_image = cv2.threshold(new_image,0,255,cv2.THRESH_BINARY_INV)
    border_width = 2
    new_image = new_image[border_width:height-border_width,border_width:width-border_width]

    return new_image

# 分割成一个个字符
def split(filename):
    # 分割颜色
    newImageFilename = extractColor(filename)
    # 清理背景
    image = clean_bg(newImageFilename)
    # 清除背景打印出来
    new_image_filename = 'cleanbgImgs/'+str(uuid.uuid4())+'.png'
    cv2.imwrite(new_image_filename,image)
    # 分割图片打印结果
    col_rect = get_col_rect(image)
    for cols in col_rect:
        block_image = get_block_image(image,cols)

        if block_image is not None:
            new_image_filename = 'letters/'+str(uuid.uuid4())+'.png'
            cv2.imwrite(new_image_filename,block_image)


def main():
    for filename in os.listdir('captchas'):
        current_file = 'captchas/' + filename
        if os.path.isfile(current_file):
            split(current_file)

if __name__ == '__main__':
    main()
