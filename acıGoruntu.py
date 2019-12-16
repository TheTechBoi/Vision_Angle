#CYMURGHSS <3

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

cam_angle = 60
cam_width = 1280

cam_center = cam_width/2
cam_centerAngle = cam_angle/2
ratio = cam_angle / cam_width

x_difference = 0
angle_difference = 0

#renkler
lower_color =  np.array([28, 100, 100])
upper_color =  np.array([48, 255, 255])

while 1:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    kernel = np.ones((15,15),np.float32)/225
    
    smoothed = cv2.filter2D(hsv,-1,kernel)

    hsv_blur = cv2.medianBlur(smoothed,15)
    

    
    mask = cv2.inRange(hsv_blur, lower_color, upper_color)

    mask = cv2.erode(mask,kernel,iterations =2)
    mask = cv2.dilate(mask,kernel, iterations=2) 

    res = cv2.bitwise_and(frame,frame, mask = mask)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) 
    
    #Yukarıda: Gerekli  format değiştirilmesi maskeleme blurlama vb.
    
    
    #Sınırları belirleme
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None 

    #frame2 = frame.copy()
    #cv2.drawContours(frame2, cnts, -1 ,(0,255,0), 3) 

    if len(cnts) > 0:

            
            c = max(cnts,key =cv2.contourArea) #buyuk değerin seçimi
	
            ((x, y), radius) = cv2.minEnclosingCircle(c) #en küçük kapsayan çember
            M = cv2.moments(c) #şekil hakkında bilgi çıkarımı
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) #bilgilerle merkezin bulunması
		     
                     
            if radius >= 5: 
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 140, 255), 6)
                cv2.circle(frame, center, 6, (255, 0, 0), -1)

                x_difference = cam_center - x
                angle_difference = 0-(x_difference*ratio)
                
                

                
            else:
                x = 0
                y = 0

    else:
        x = 0
        y = 0

    print("x : ")
    print(x)
    print("y : ")
    print(y) 
    print("Angle : ")
    print(angle_difference)
    
        
    cv2.imshow('OHA',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27: 
        break
    
      
 
cv2.destroyAllWindows() 
cap.release()
