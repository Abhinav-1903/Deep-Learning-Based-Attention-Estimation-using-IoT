from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from gaze_tracking import GazeTracking
import xlsxwriter     
import time      
book = xlsxwriter.Workbook('Example3.xlsx')     
sheet = book.add_worksheet()


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
cascade_classifier=cv2.CascadeClassifier(r'C:\Users\majaa\OneDrive\Desktop\images\haarcascade_frontalface_default.xml')
model=load_model(r'C:\Users\majaa\OneDrive\Desktop\images\face.hdf5')
class_labels=['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']
row = 0    
column = 0       
t=0
# iterating through the content list
t1=time.time()
i=0
while True:
    _, frame = webcam.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),fx=100,fy=100,interpolation=cv2.INTER_CUBIC)
        crop = frame[y:y+h,x:x+w]
        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)
            preds = model.predict(roi)[0]
            label=class_labels[preds.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),3)
            gaze.refresh(frame)
            frame = gaze.annotated_frame()
            text =""
           
          #  if gaze.is_right():
          #      text = "Not Attentive"
          #  elif gaze.is_left():
          #      text = "Not Attentive"
          #  elif gaze.is_center():
          #      text = "Attentive"
          #  elif gaze.is_blinking():
          #      text = "Not attentive"
            r_cor=gaze.is_right()
            l_cor=gaze.is_left()
            label_position = (x-2,y-50)
            if(t==0):
                t2=time.time()
            time.sleep(1)
            t3=time.time()
            t=t3-t2
            t4=t3-t1
            print(t)
            if(label=="Angry"):
                label=0.86
            elif(label=="Disgust"):
                label=-0.93
            elif(label=="Fear"):
                label=0.86
            elif(label=="Happy"):
                label=0.79
            elif(label=="Sad"):
                label=-0.90
            elif(label=="Surprise"):
                label=0.85
            elif(label=="Neutral"):
                label=-0.82
            l=[]
           # if t>5:     
            t=0
            print("12345")
            l.append(text)
            l.append(l_cor)
            l.append(gaze.vertical())
            l.append(preds.argmax())
            for x in l:
                print()
                sheet.write(row, column, x)
                column+=1
            #sheet.insert_image(row,column,roi_gray) 
            row += 1
            column=0
            cv2.putText(frame, text,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),3)
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            cv2.imshow("Demo", frame)
            cv2.imwrite('kang'+str(i)+'.jpg',crop)
            sheet.insert_image(row,column,'kang'+str(i)+'.jpg')            
            i+=1
    if cv2.waitKey(1) == 27:
        book.close()
        break
