from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import numpy as np

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import cv2.aruco as aruco
import numpy as np
import rectangleArea as ra
import math

# reding calibration matrices

calibrationResultPath = "res//"

fsContent = cv2.FileStorage(calibrationResultPath + "calibrationValues0.yaml", cv2.FILE_STORAGE_READ)

mtxNode = fsContent.getNode('camera_matrix')
distNode = fsContent.getNode('dist_coeff')

mtx = np.asarray(mtxNode.mat())
distor = np.asarray(distNode.mat())

print("--------------------")
print(mtx)
print("--------------------")
print(distor)
print("--------------------")

# mtx = np.array([[2.6822003708394282e+03, 0., 1.5588865381021240e+03], [0., 2.6741978758743703e+03, 1.2303469240154550e+03], [0., 0., 1.]])
# distor = np.array([2.0426196677407879e-01, -3.3902097431574091e-01, -4.1813964792274307e-03, -1.0425257413809015e-02, 8.2004709580884308e-02])

# getting ready the aruco dictionary

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# opening rpi camera

camera = PiCamera()
# camera.resolution = (1040, 784)
camera.resolution = (1024, 770)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1024, 770))

time.sleep(0.1)

tvec0 = np.array([[[0.0, 0.0, 0.0]]])

rvecmax = 0.0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.rectangle(image, (0, 0), (200, 200), (220, 240, 230), -1)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(image, aruco_dict)
    image = aruco.drawDetectedMarkers(image, corners)  # marker körvonalak

    rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, distor)

    # rvec = np.array([[[0.0, 0.0, 0.0]]])

    if ids is not None:
        for i in range(0, ids.size):
            # print(image.dtype)
            rr, thet = ra.rArea(corners)
            aruco.drawAxis(image, mtx, distor, rvec[0], tvec[0], 0.06)  # np.array([0.0, 0.0, 0.0])
            # print(f, "\t", end = " ")
            # print("%d táv: %.2f" % (i, math.sqrt(rvec[i][0][0]**2 + rvec[i][0][1]**2 + rvec[i][0][2]**2)))
            # cv2.putText(image, image.shape())
            # cv2.putText(image, "%.1f cm" % ((20000 / rr**0.5) * 0.116 - 2.08), (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (244, 244, 244))
            cv2.putText(image, "%.1f cm -- %.0f deg" % ((tvec[0][0][2] * 100), (rvec[0][0][2] / math.pi * 180)),
                        (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (244, 244, 244))
            cv2.circle(image, (100, int(rr / 600)), 6, (200, 40, 230), -1)
            R, _ = cv2.Rodrigues(rvec[0])
            cameraPose = -R.T * tvec[0]
            # print(type(cameraPose))
            # print((int)(tvec[0][0][2] * 1000))
            # rvec = red, blue, green
            """
            if ((rvec[0][0][1])) > rvecmax:
                rvecmax = (rvec[0][0][1]);
            print((int)(rvec[0][0][0] / math.pi * 180), " ", (int)(rvec[0][0][1] / math.pi * 180), " ", (int)(rvec[0][0][2] / math.pi * 180))
            #print(rvec.shape)
            """

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break