import time # added import for time
from djitellopy import tello
import keyboardcontrol as kc
import numpy as np
import cv2
import math

# added missing variables
yaw = 0
x = 500
y = 500
angle = 0

#####parameters ####
fspeed= 117/10# forward speed in cm/s (14cm/s)
aspeed = 360/10# Angular speed degreees/s (40d/s)
interval = 0.25

dinterval=fspeed*interval
aaInterval=aspeed*interval
######################################################

me = tello.Tello()
me.connect()
print(me.get_battery())

points =[]

def getkeyboardinput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 14
    anglespeed=40
    global yaw
    global x
    global y
    global angle
    d= 0

    # '''negative speed and postive speed'''
    if kc.getkey("Left"):
        lr = -speed
        d=dinterval
        angle= -100
    elif kc.getkey("Right"):
        lr = speed
        d = -dinterval
        angle = 180

    if kc.getkey("UP"):
        fb = speed
        d = dinterval
        angle = 270

    if kc.getkey("Down"):
        fb = -speed
        d = -dinterval
        angle = -90

    if kc.getkey("W"):
        ud = speed
    elif kc.getkey("S"):
        ud = -speed

    # rotation
    if kc.getkey("a"):
        yv = -anglespeed
        yaw-= aaInterval
    elif kc.getkey("d"):
        yv = anglespeed
        yaw += aaInterval

    if kc.getkey("q"):
        me.land() # added landing function call
        return 0,0,0,0,x,y # added return statement to stop the loop
    if kc.getkey("e"):
        me.takeoff() # added take off function call
        return 0,0,0,0,x,y # added return statement to stop the loop

    time.sleep(interval) # added sleep function

    angle =+ yaw
    x += int(d*math.cos(math.radians(angle)))
    y += int(d*math.sin(math.radians(angle)))
    return lr, fb, ud, yv,x,y


def drawmap(img,points):
    for point in points:
        cv2.circle(img,(point[0],point[1]), 5,(0,0,255), cv2.FILLED)
    cv2.putText(img,f'({(points[-1][0]-500)/100},{(points[-1][1]-500)/100})m',
                (points[-1][0]+10 ,points[-1][1]+30),cv2.FONT_HERSHEY_SIMPLEX,1,
                (255,0,255),1)

while True:
    vals = getkeyboardinput()
    if vals[0] == 0 and vals[1] == 0 and vals[2] == 0 and vals[3] == 0: # added condition to check if drone is landed or taken off
        break
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000,1000,3),np.uint8)
    if (points[-1][0]!= vals[4] or points[-1][1]!=vals[5]):
        points.append((vals[4], vals[5]))
    drawmap(img,points)
    cv2.imshow("output",img)
    key = cv2.waitKey(1)
    if key == ord('q'): # added condition to close the window
        break

cv2.destroyAllWindows() # added function to close the window
me.end() # added function to end the connection

#This script is used to control a Tello drone using keyboard inputs.
# The script uses the djitellopy and keyboardcontrol libraries to connect to the drone and
# receive input from the keyboard. The script also uses the numpy and
# cv2 libraries for image processing. The script defines several parameters such as forward speed,
# angular speed, and interval for controlling the drone's movement.
# The script then uses a while loop to continuously check for keyboard inputs and
# send them to the drone as control commands. It also uses the OpenCV library to create a visual
# representation of the drone's movement on a map.
