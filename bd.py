# BEHAVIOUR DETECTION USING BODY PARTS ARRAYS
# FOR IMAGES ONLY

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import sys
import math



net=cv.dnn.readNetFromTensorflow("/Users/Skanda/Desktop/YYOOLLOO/finalPOSE/graph_opt.pb")

inWidth=368
inHeight=368
thr=0.2

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                   "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                   "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                   ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                   ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                   ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]



img=cv.imread("/Users/Skanda/Desktop/YYOOLLOO/finalPOSE/pose1.jpg")
cv.imshow("q",img)

def pose_estimation(frame):
    frameWidth=frame.shape[1]
    frameHeight=frame.shape[0]
    net.setInput(cv.dnn.blobFromImage(frame,1.0,(inWidth,inHeight),(127.5,127.5,127.5), swapRB=True, crop=False))
    out=net.forward()
    out=out[:, :19, :, :]


    #-------------------

   

    #---------------------

    assert(len(BODY_PARTS) == out.shape[1])

    points=[]


    for i in range(len(BODY_PARTS)):
        heatMap=out[0, i, :, :]

        _, conf, _, point=cv.minMaxLoc(heatMap)
        x=(frameWidth*point[0])/out.shape[3]
        y=(frameHeight*point[1])/out.shape[2]
        points.append((int(x), int(y)) if conf > thr else None)


    for pair in POSE_PAIRS:
        partFrom=pair[0]
        partTo=pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom=BODY_PARTS[partFrom]
        idTo=BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)


    t, _=net.getPerfProfile()
    freq=cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return frame







# ---------------------------------------------------------



#-------------------------------------------------






eImage=pose_estimation(img)



cv.imshow("OUTPUT",eImage)
cv.waitKey(0)
cv.destroyAllWindows()













































