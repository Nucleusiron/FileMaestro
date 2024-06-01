import mouse
import cv2
import time
screen_w = 0
screen_h = 0


while True:
    if screen_w < mouse.get_position()[0]:
        screen_w = mouse.get_position()[0]
    if screen_h < mouse.get_position()[1]:
        screen_h = mouse.get_position()[1]

    
    path = 'D:\Final_Project\Waiting.jpeg'
  
    # Reading an image in default mode 
    image = cv2.imread(path) 
    
    # Window name in which image is displayed 
    window_name = 'Calibration'
    
    # Using cv2.imshow() method 
    # Displaying the image 

    cv2.imshow(window_name, image) 

    key1 = cv2.waitKey()

    if key1 == ord("q"):
        break
print(screen_w,"\n", screen_h)
cv2.destroyAllWindows()
