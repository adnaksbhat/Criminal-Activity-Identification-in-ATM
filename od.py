import cv2
import numpy as np

net=cv2.dnn.readNet('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/yolov3_training_last.weights','/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/yolov3_testing.cfg')
classes=[]
with open('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/classes.txt','r') as f:
    classes=f.read().splitlines()

#print(classes)


count=0


#img=cv2.imread('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/nomask.jpg')
#img=cv2.imread('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/fmask.jpg')
#img=cv2.imread('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/hel.jpeg')
#img=cv2.imread('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/knife1.jpg')
img=cv2.imread('/Users/Skanda/Desktop/YYOOLLOO/Z_THIS/gun3.jpg')

img=cv2.resize(img,(1280,720))
height, width, _ = img.shape



blob=cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

#for b in blob:
 #   for n, img_blob in enumerate(b):
  #      cv2.imshow(str(n), img_blob)


net.setInput(blob)

output_layers_names=net.getUnconnectedOutLayersNames()
layerOutputs=net.forward(output_layers_names)


boxes=[]
confidences=[]
class_ids=[]

for output in layerOutputs:
    for detection in output:
        scores=detection[5:]
        class_id=np.argmax(scores)
        confidence=scores[class_id]
        if confidence>0.5:
            center_x=int(detection[0]*width)
            center_y=int(detection[1]*height)
            w=int(detection[2]*width)
            h=int(detection[3]*height)

            x=int(center_x - w/2)
            y=int(center_y - h/2)

            boxes.append([x, y, w, h])
            confidences.append((float(confidence)))
            class_ids.append(class_id)


indexes=cv2.dnn.NMSBoxes(boxes,confidences, 0.5, 0.4)
font=cv2.FONT_HERSHEY_PLAIN
colors=np.random.uniform(0, 255, size=(len(boxes), 3))

for i in indexes.flatten():
    x, y, w, h = boxes[i]
    str1="Wearing Mask"
    str2="Not wearing Mask"
    str3="Helmet"
    str4="Knife"
    str5="Gun"
    
    label=str(classes[class_ids[i]])
    confidence=str(round(confidences[i],2))
    color=colors[i]
    cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
    cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)
    count=count+1
    
    
    if label==str1:
        if count>1:
            print("1 person at a time please")
            break
        print("Remove mask")
    elif label==str2:
        if count>1:
            print("1 person at a time please")
            break
        elif count==1:
            print("proceed transactions")
    elif label==str3:
        print("Remove helmet")
    elif label==str4:
        print("Weapon detected") 
    elif label==str5:
        print("Weapon detected")      


    
    









cv2.imshow('Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()