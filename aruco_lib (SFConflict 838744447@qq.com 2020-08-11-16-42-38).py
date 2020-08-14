import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math

'''
该文件中的功能：
* angle_calculate（pt1，pt2，trigger = 0）-函数返回两点之间的角度
* detect_Aruco（img）-返回ID为：corners的检测到的aruco列表字典
* mark_Aruco（img，aruco_list）-标记中心并显示ID的功能
* compute_Robot_State（img，aruco_list）-给出机器人的状态（中心（x），中心（y），角度）
'''

def angle_calculate(pt1,pt2, trigger = 0):  # 该函数返回两点之间的角度，范围为0-359
    angle_list_1 = list(range(359,0,-1))
    #angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # 打开元组
    y=pt2[1]-pt1[1]
    angle=int(math.degrees(math.atan2(y,x))) #取2点并相对于水平轴的角度范围为（-180,180）
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    return int(angle)

def detect_Aruco(img):  #返回ID为：corners的检测到的aruco列表字典
    aruco_list = {}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)   #创建6×6aruco字典  0-249
    parameters = aruco.DetectorParameters_create()  #请参考opencv页面进行
    #检测ID列表以及每个ID的边角
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    #角是检测到的标记的角（numpy数组）的列表。 对于每个标记，其四个角均按其原始顺序返回（从左上角开始顺时针旋转）。 因此，第一个角是左上角，然后是右上角，右下角和左下角。
    # print corners[0]
    #gray = aruco.drawDetectedMarkers(gray, corners,ids)
    #cv2.imshow('frame',gray)
    #print (type(corners[0]))
    if len(corners):    #返回aurco个数
        #print (len(corners))
        #print (len(ids))
        print (type(corners))
        print (corners[0][0])
        for k in range(len(corners)):
            temp_1 = corners[k]
            temp_1 = temp_1[0]
            temp_2 = ids[k]
            temp_2 = temp_2[0]
            aruco_list[temp_2] = temp_1

        return aruco_list

def mark_Aruco(img, aruco_list):    #标记中心并显示ID的功能
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry是形状为（4,2）的numpy数组
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#所以是numpy数组，加法不是列表加法
        centre[:] = [int(x / 4) for x in centre]    #寻找中心
        #print centre
        orient_centre = centre + [0.0,5.0]
        #print orient_centre
        centre = tuple(centre)
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        #print centre
        #print orient_centre
        cv2.circle(img,centre,1,(0,0,255),8)
        #cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
        #cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
        #cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
        #cv2.circle(img,orient_centre,1,(0,0,255),8)
        cv2.line(img,centre,orient_centre,(255,0,0),4) #marking the centre of aruco
        #cv2.line(img,centre,orient_centre,(255,0,0),4)
        cv2.putText(img, str(key), (int(centre[0] + 20), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA) # displaying the idno
    return img

def calculate_Robot_State(img,aruco_list):  #给出机器人的状态（中心（x），中心（y），角度）
    robot_state = {}
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for key in key_list:
        dict_entry = aruco_list[key]
        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
        centre[:] = [int(x / 4) for x in centre]
        centre = tuple(centre)
        #打印中心
        angle = angle_calculate(pt1, pt2)
        cv2.putText(img, str(angle), (int(centre[0] - 80), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
        robot_state[key] = (int(centre[0]), int(centre[1]), angle)#但是，如果您要缩放图像并进行全部...更好地反转X和Y ...那么，那么只有比例相同
    #print (robot_state)

    return robot_state