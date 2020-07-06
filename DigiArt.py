from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import sys
import urllib
img1=cv2.imread('shot.jpg')
gray1=cv2.imread('shapes1.jpg',0)
ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the (optional) video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="max buffer size")
args=vars(ap.parse_args())
#
redLower=(23,59,119)
redUpper=(54,255,255)
#
pts=deque(maxlen=args["buffer"])
counter=0
(dX,dY)=(0,0)
direction=""
#
cam=cv2.VideoCapture(0)
radius=0
#
while True:
    st,frame=cam.read()
    #
    frame=imutils.resize(frame,width=600)
    #
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #
    mask=cv2.inRange(hsv,redLower,redUpper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    #
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center=None
    #
    if len(cnts) > 0:
       #
       c=max(cnts,key=cv2.contourArea)
       ((x,y),radius)=cv2.minEnclosingCircle(c)
       M=cv2.moments(c)
       center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
       #
    if radius>10:
       #
       cv2.circle(frame,(int(x),int(y)),int (radius),(0,255,255),2)
       cv2.circle(frame,center,5,(0,0,255),-1)
       pts.appendleft(center)
    for i in np.arange(1,len(pts)):
       #
       if pts[i-1] is None or pts[i] is None:
           continue
       if counter>=200 and i==1 and pts[-10] is not None:
           #
           dX=pts[-10][0]-pts[i][0]
           dY=pts[-10][1]-pts[i][1]
           (dirX,dirY)=("","")
          #
           if np.abs(dX)>20:
               dirX="East" if np.sign(dX)==1 else "West"
               #
           if np.abs(dY)>20:
               dirY="North" if np.sign(dY)==1 else "South"
           if dirX!="" and dirY!="":
               direction= "{}-{}".format(dirY,dirX)
               #
           else:
               direction=dirX if dirX !="" else dirY
       thickness=int (np.sqrt(args["buffer"]/float (i+1)) *2.5)
       cv2.line(frame,pts[i-1],pts[i],(255,0,0),thickness)
       #
    cv2.putText(frame,direction,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),3)
    cv2.putText(frame,"dx: {},dy: {}".format(dX,dY),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1) & 0xFF
    counter+=1
    if key==ord("q"):
        break
img1.release()
cv2.destroyAllWindows()
    

