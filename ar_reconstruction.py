#by zengwenjian123
'''
利用ar标签估算相机位置

'''

import cv2
import glob
import cv2.aruco as aruco


frame_name=glob.glob('./pic/*.jpg')#搜索目录下所有的jpg图片
for fname in frame_name:
    img=cv2.imread(fname)
    img1=img
    img=cv2.resize(img,None,fx=1,fy=1,interpolation=cv2.INTER_CUBIC)
    #灰度化
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #设置预定义字典
    aruco_dict=aruco.Dictionary_get(aruco.DICT_6X6_250)
    # 使用默认值初始化检测器参数
    parameters = aruco.DetectorParameters_create()
    # 使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)

    print('corner:',corners,'ids:',ids,'rejectedImgPoints',rejectedImgPoints)
    # 将detectMarkers函数返回的标记轮廓[0][0]点numpy数组转换为int

    for i in range(ids.size):
        print(i)
        print(ids[i])
        # 将detectMarkers函数返回的标记轮廓[0][0]点numpy数组转换为int
        print(int(corners[i][0][0].tolist()[0]), int(corners[i][0][0].tolist()[1]))
        #print(corners)
        cv2.circle(img1, (int(corners[i][0][0].tolist()[0]), int(corners[i][0][0].tolist()[1])), 5, (0, 0, 255), -1)
        #print(int(corners[i][0][0].tolist()[0]), int(corners[i][0][0].tolist()[1]),int(corners[i][0][1].tolist()[0]), int(corners[i][0][1].tolist()[1]))
        marker_x=int(corners[i][0][0].tolist()[0]), int(corners[i][0][0].tolist()[1])
        marker_y=int(corners[i][0][1].tolist()[0]), int(corners[i][0][1].tolist()[1])
        marker_z=int(corners[i][0][2].tolist()[0]), int(corners[i][0][2].tolist()[1])
        print(marker_x,marker_y,marker_z)
        cv2.putText(img1, str(ids[i]), (int(corners[i][0][0].tolist()[0]), int(corners[i][0][0].tolist()[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    # 画出标志位置
    aruco.drawDetectedMarkers(img1, corners, ids)





    cv2.imshow('frame',img1)
    cv2.waitKey(1200)
