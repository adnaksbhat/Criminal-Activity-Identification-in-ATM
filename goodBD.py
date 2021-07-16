# BEHAVIOUR DETECTION USING MEDIAPIPE(pre-trained)





import cv2
import mediapipe as mp
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



from datetime import datetime

 
# dd/mm/YY H:M:S
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	





def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle




cap = cv2.VideoCapture(0)
#cap=cv2.VideoCapture('/Users/Skanda/Desktop/YYOOLLOO/finalPOSE/vd.mp4')

flag=0
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        #frame = cv2.resize(frame, None, None, fx=0.5, fy=0.5)      ---------> resize vdo
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            hipL=  [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]


            shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            hipR=  [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]


            kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankleL = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankleR = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            


            
            
            
            # Calculate angle
            
            angle1 = calculate_angle(hipL, shoulderL, elbowL)
            if angle1>160:
                flag=flag+1
                if flag>30:
                    print("ABNORMAL DETECTED shL->",angle1,"------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break



            angle2 = calculate_angle(hipR, shoulderR, elbowR)
            if angle2>160:
                flag=flag+1
                if flag>30:
                    print("ABNORMAL DETECTED shR ->",angle2,"------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break

            angle3 = calculate_angle(hipR, kneeR, ankleR)
            if angle3<50:
                flag=flag+1
                if flag>16:
                    print("ABNORMAL DETECTED kR","------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break

            angle4 = calculate_angle(hipL, kneeL, ankleL)
            if angle4<50:
                flag=flag+1
                if flag>16:
                    print("ABNORMAL DETECTED KL","------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break

            
            angle5 = calculate_angle(shoulderL, hipL, ankleL)
            if angle5<140:
                flag=flag+1
                if flag>16:
                    print("ABNORMAL DETECTED hip","------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break

            
            angle6 = calculate_angle(shoulderR, hipR, ankleR)
            if angle6<140:
                flag=flag+1
                if flag>16:
                    print("ABNORMAL DETECTED hip","------------------",dt_string)
                    os.system('python /Users/Skanda/Desktop/YYOOLLOO/finalPOSE/warn.py')
                    break


                

            
                
            
            # Visualize angle
            cv2.putText(image, str(int(angle1)), 
                           tuple(np.multiply(shoulderL, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(int(angle2)), 
                           tuple(np.multiply(shoulderR, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(int(angle3)), 
                           tuple(np.multiply(kneeR, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(int(angle4)), 
                           tuple(np.multiply(kneeL, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(int(angle5)), 
                           tuple(np.multiply(hipL, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(int(angle6)), 
                           tuple(np.multiply(hipR, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )


            
                       
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=3), 
                                mp_drawing.DrawingSpec(color=(0,255,255), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('=------------------------------------CCTV ATM VIEW------------------------------------=', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()