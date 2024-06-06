import threading
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import mouse
import keyboard
import time
import notifier
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Threads------------------------------------------------------------

l_delay = 0
r_delay = 0
l_double_delay = 0
left_delay = 0
right_delay = 0
mode_delay = 0
copy_delay = 0
cut_delay = 0
paste_delay = 0
space_delay = 0

def l_clk_delay():
    global l_delay
    global l_clk_thread
    time.sleep(0.5)
    l_delay = 0
    l_clk_thread = threading.Thread(target=l_clk_delay)

l_clk_thread = threading.Thread(target = l_clk_delay)

def r_clk_delay():
    global r_delay
    global r_clk_thread
    time.sleep(0.5)
    r_delay = 0
    r_clk_thread = threading.Thread(target = r_clk_delay)

r_clk_thread = threading.Thread(target = r_clk_delay)

def l_double_clk_delay():
    global l_double_delay
    global l_double_clk_thread
    time.sleep(0.5)
    l_double_delay = 0
    l_double_clk_thread = threading.Thread(target = l_double_clk_delay)

l_double_clk_thread = threading.Thread(target = l_double_clk_delay)

def right_kb_delay():
    global right_delayw
    global right_thread
    time.sleep(1)
    right_delay = 0
    right_thread = threading.Thread(target = right_kb_delay)

right_thread = threading.Thread(target = right_kb_delay)

def left_kb_delay():
    global left_delay
    global left_thread
    time.sleep(1)
    left_delay = 0
    left_thread = threading.Thread(target = left_kb_delay)

left_thread = threading.Thread(target = left_kb_delay)

def mode_change_delay():
    global mode_delay
    global mode_thread
    time.sleep(5)
    mode_delay = 0
    mode_thread = threading.Thread(target = mode_change_delay)

mode_thread = threading.Thread(target = mode_change_delay)

def copy_click_delay():
    global copy_delay
    global copy_thread
    time.sleep(1)
    copy_delay = 0
    copy_thread = threading.Thread(target = copy_click_delay)

copy_thread = threading.Thread(target = copy_click_delay)

def cut_click_delay():
    global cut_delay
    global cut_thread
    time.sleep(1)
    cut_delay = 0
    cut_thread = threading.Thread(target = cut_click_delay)

cut_thread = threading.Thread(target = cut_click_delay)

def paste_click_delay():
    global paste_delay
    global paste_thread
    time.sleep(1)
    paste_delay = 0
    paste_thread = threading.Thread(target = paste_click_delay)

paste_thread = threading.Thread(target = paste_click_delay)

def space_click_delay():
    global space_delay
    global space_thread
    time.sleep(1)
    space_delay = 0
    space_thread = threading.Thread(target = space_click_delay)

space_thread = threading.Thread(target = space_click_delay)


# Mode Changing------------------------------------------------------------

mode = 0
modes =['mouse', 'watching']
mode_change = True

def mouse_mode_change():
    global mode
    global modes
    if mode == 0:
        mode = 1
    else:
        mode = 0
    notifier.change_mod_notifier(modes[mode])


# Camera setup------------------------------------------------------------

cam_w, cam_h = 960, 720
cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

#fps
pTime = 0
frameX = 100
frameY = 175
frameY2 = 25


# Volume setup------------------------------------------------------------

sound_changing = False
sound_range = cam_h//3
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
min_volume, max_volume, temp = volume.GetVolumeRange()


# Hand detection------------------------------------------------------------

detector = HandDetector(detectionCon = 0.8, maxHands =1)
"""
#import os
# running other file using run()
#os.system("python calibration.py")

#with open("calibration.py") as file:
#    exec(file.read())
process = subprocess.Popen(["python", "calibration.py"])
screen_w = calibration.screen_w
screen_h = calibration.screen_h
cv2.destroyAllWindows()
#process.kill()"""

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands , img = detector.findHands(img, flipType=False)

    if hands:
        lmlist = hands[0]['lmList']
        #Frame rate
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img, str(int(fps)), (20,50),cv2.FONT_HERSHEY_PLAIN,3,
                    (255,0,0),3)
        cv2.rectangle(img, (frameX, frameY2), (cam_w - frameX, cam_h - frameY), (255, 0, 255), 2)

        fingers = detector.fingersUp(hands[0])
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        tum_x, tum_y = lmlist[4][0], lmlist[4][1]
        mid_x, mid_y = lmlist[12][0], lmlist[12][1]


        #Mode changer
        if fingers == [0,0,1,1,1]:
            cv2.putText(img, f"Mode Changing", (cam_w//2,cam_h//2),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)            
            if np.sqrt((tum_x - ind_x)**2 + (tum_y - ind_y)**2) < 35:
                if mode_delay == 0:
                    mouse_mode_change()    
                    mode_delay = 1
                    mode_thread.start()
        #Mouse mod
        if mode == 0:

            #Mouse movement        
            if fingers == [1,1,0,0,0]:

                mouse_x = int(np.interp(ind_x, (frameX, cam_w - frameX), (0, 1920)))
                mouse_y = int(np.interp(ind_y, (frameY2, cam_h - frameY), (0, 1080)))
                mouse.move(mouse_x,mouse_y)
            
            #Mouse left click
            elif fingers == [1,1,1,0,0]:
                if np.sqrt((mid_x - ind_x)**2 + (mid_y - ind_y)**2) < 35:
                    if l_delay == 0:
                        mouse.click(button="left")
                        l_delay = 1
                        l_clk_thread.start()

            #Mouse right click
            elif fingers == [1,1,1,0,1]:
                if np.sqrt((mid_x - ind_x)**2 + (mid_y - ind_y)**2) < 35:
                    if r_delay == 0:
                        mouse.click(button="right")
                        r_delay = 1
                        r_clk_thread.start()

            #Mouse left deouble click
            elif fingers == [0,1,1,0,0]: #Change it
                if np.sqrt((mid_x - ind_x)**2 + (mid_y - ind_y)**2) < 35:
                    if l_double_delay == 0:
                        mouse.double_click(button="left")
                        l_double_delay = 1
                        l_double_clk_thread.start()
            
            #Mouse scroll Down
            elif fingers == [1,0,0,0,1]: #Change it           
                mouse.wheel(delta = -1)
            
            #Mouse scroll Up
            elif fingers == [0,0,0,0,0]: #Change it           
                mouse.wheel(delta = 1)
            
            #Copy
            elif fingers == [0,1,0,0,0]: #Change it           
                if copy_delay == 0:
                    keyboard.press_and_release('ctrl+c')
                    copy_delay = 1
                    copy_thread.start()
            #Cut
            elif fingers == [1,0,0,1,1]: #Change it           
                if cut_delay == 0:
                    keyboard.press_and_release('ctrl+x')
                    cut_delay = 1
                    cut_thread.start()
            #Paste
            elif fingers == [1,1,1,1,1]: #Change it           
                if paste_delay == 0:
                    keyboard.press_and_release('ctrl+v')
                    paste_delay = 1
                    paste_thread.start()
            
            
        #Watching video mod 
        elif mode == 1:
            
            #Sound settings
            if fingers == [1,1,1,0,0]:
                if np.sqrt((mid_x - ind_x)**2 + (mid_y - ind_y)**2) < 35:
                    if not sound_changing:
                        start_volume = volume.GetMasterVolumeLevel()
                        start_y = mid_y 
                    sound_changing = True
                    print(start_volume)
                    change = -(mid_y - start_y) #I pu t minus because index start from top
                    start_change = np.interp((start_volume), [min_volume, max_volume], [-sound_range*3/7, sound_range*3/7])
                    vol = np.interp((change+start_change), [-sound_range*3/7, sound_range*3/7], [min_volume, max_volume])
                    #volume.GetMute()
                    volume.SetMasterVolumeLevel(vol, None)

                else:
                    sound_changing = False    
            #Mute
            elif np.sqrt((mid_x - ind_x)**2 + (mid_y - ind_y)**2) < 35 and np.sqrt((tum_x - ind_x)**2 + (tum_y - ind_y)**2) < 35 and np.sqrt((mid_x - tum_x)**2 + (mid_y - tum_y)**2) < 35 and fingers[3] == 0 and fingers[4] == 0:
                volume.SetMasterVolumeLevel(min_volume, None)
            
            #arrow
            elif fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
                #left arrow
                if fingers[0] == 0 and fingers[4] == 0:
                    
                    if left_delay == 0:
                        keyboard.press_and_release('left')
                        left_delay = 1
                        left_thread.start()
                        
                #right arrow
                elif fingers[0] == 1 and fingers[4] == 1:
                    
                    if right_delay == 0:
                        keyboard.press_and_release('right')
                        right_delay = 1
                        right_thread.start()

            elif fingers == [0,1,1,1,1]:
                if space_delay == 0:
                    keyboard.press_and_release('space')
                    space_delay = 1
                    space_thread.start()


        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 100), 2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('w'):  
        break


    