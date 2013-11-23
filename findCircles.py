import cv2
import cv2.cv as cv
import numpy as np
from operator import itemgetter, attrgetter

img = cv2.imread('image3.jpg',0)
img1 = cv2.imread('image3.jpg',1)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=20,maxRadius=40)

circles = np.uint16(np.around(circles))

pieces=[]
xs=[]
ys=[]

for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)

    bgr=(0,0,0)
    for a in range (-3,4):
    	for b in range (-3,4):
    		c=img1[i[1]+a*4,i[0]+b*4]
    		bgr=(int(c[0])+bgr[0],int(c[1])+bgr[1],int(c[2])+bgr[2])
    bgr=(bgr[0]/49,bgr[1]/49,bgr[2]/49)

    cv2.circle(cimg,(i[0],i[1]),3,bgr,3)


    pieces.append((i[1],i[0],bgr))


sortedy=sorted(pieces, key=itemgetter(1))
board=[]
for i in range(7):
	column=sortedy[i*6:(i+1)*6]
	column=sorted(column, key=itemgetter(0), reverse=True)
	board.append(column)

baseyellow=board[3][0][2]
basered=board[3][1][2]

threshold = 45

outputBoard=[[[] for _ in range(6)] for _ in range(7)]
for b in range(len(board)):
	for a in range(len(board[b])):
		bgr=board[b][a][2]
		yerror = abs(bgr[0]-baseyellow[0])+abs(bgr[1]-baseyellow[1])+abs(bgr[2]-baseyellow[2])
		rerror = abs(bgr[0]-basered[0])+abs(bgr[1]-basered[1])+abs(bgr[2]-basered[2])
		print str(b)+" "+str(a)+" " + str(board[b][a])+ " " + str(yerror) + " " + str(rerror)

		if yerror<threshold:
			outputBoard[b][a]=0
		elif rerror<threshold:
			outputBoard[b][a]=1
s=""
for x in outputBoard:
	for y in x:
		s+=str(y)
	s+="\n"
print s

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()