import cv2
import numpy as np
import math
import string
import path

#crops an image by given corners
def crop(im, x1, y1, x2, y2):
    
    size = 10
    crop_img = im[y1-size:y2+size, x1-size:x2+size]
    return crop_img


#returns the letters for the flags of an image 
def corners(im):
    c = []
    cx = set()
    cy = set()
    flags = []
    sqPt = []
    otherC = []
    letters = []
    
    image = cv2.imread(im)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray = np.float32(gray)
    
    corner = cv2.goodFeaturesToTrack(gray, 100, 0.75, 20,3)
    
    corner = np.int0(corner)
    

    for i in corner[0:]:
        x, y = i.ravel()
        
        cv2.circle(image,(x,y),3,(0,255,0),0)
        
        for i in range (-10, 10):
            if (x+i) in cx:
                x = x+i
            if (y+i) in cy:
                y = y+i
        cx.add(x)
        cy.add(y)
        c.append([x,y])
    
    c = sorted(c)

    cx = sorted(list(cx))
    cy = sorted(list(cy))
    
    #print(cx)
    #print(cy)
    
    dx = abs(cx[1] - cx[0])
    dy = abs(cy[1] - cy[0])
    
    scale = 225/dx
    resize = (math.ceil(image.shape[1] * scale), math.ceil(image.shape[0] * scale))
    
    
    resized = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)

    for i in range(len(cy)//2):

        flags.append(crop(image, cx[0], cy[0+(2*i)], cx[1], cy[1+(2*i)]))
        
    for j in flags:
       
        letters.append(everyFlag(j)[1])
        
    #print(letters)
    
    return letters
    
#checks if the given flag is India (for false positives with Sierra)
def isolateIndia(image):
    isIndia = False
    
    y = ([0,50,100], [100,255,255])

    lowerY = np.array(y[0], dtype = "uint8")
    upperY = np.array(y[1], dtype = "uint8")
  
    yellow = cv2.inRange(image, lowerY, upperY)
    
    imYellow = cv2.bitwise_and(image, image, mask = yellow)

    num = cv2.countNonZero(yellow)
    
   
    if num > 30000:
        isIndia = True
    
    return isIndia
    
#checks if the given flag is Echo (for false positives)
def isolateEcho(image):
    isEcho = False
    
    r = ([17,15,100], [50,56,200])
    b = ([86, 31, 0], [220,88,50])

    lowerR = np.array(r[0], dtype = "uint8")
    upperR = np.array(r[1], dtype = "uint8")
    lowerB = np.array(b[0], dtype = "uint8")
    upperB = np.array(b[1], dtype = "uint8")
  
    red = cv2.inRange(image, lowerR, upperR)
    blue = cv2.inRange(image, lowerB, upperB)
    
    imRed = cv2.bitwise_and(image, image, mask = red)
    imBlue = cv2.bitwise_and(image, image, mask = blue)


    numRed = cv2.countNonZero(red)

    numBlue = cv2.countNonZero(blue)

   
    if numRed > 17000 and numBlue > 17000:
        isEcho = True
    
    return isEcho
    
#checks if the given flag is Hotel (for false positives)
def isolateHotel(image):
    isHotel = False
    
    r = ([17,15,100], [100,56,255])

    lowerR = np.array(r[0], dtype = "uint8")
    upperR = np.array(r[1], dtype = "uint8")
  
    red = cv2.inRange(image, lowerR, upperR)
    
    imRed = cv2.bitwise_and(image, image, mask = red)


    num = cv2.countNonZero(red)

    if num > 17000:
        isHotel = True
    
    return isHotel

#checks if the given flag is Charlie (for confusion with Juliet)
def isolateCharlie(image):
    isCharlie = False
    
    r = ([17,15,100], [50,56,200])
    b = ([86, 31, 0], [220,88,50])

    lowerR = np.array(r[0], dtype = "uint8")
    upperR = np.array(r[1], dtype = "uint8")
    lowerB = np.array(b[0], dtype = "uint8")
    upperB = np.array(b[1], dtype = "uint8")
  
    red = cv2.inRange(image, lowerR, upperR)
    blue = cv2.inRange(image, lowerB, upperB)
    
    imRed = cv2.bitwise_and(image, image, mask = red)
    imBlue = cv2.bitwise_and(image, image, mask = blue)


    num = cv2.countNonZero(red)

   
    if num > 7000:
        isCharlie = True
    
    return isCharlie
    
#compares the image against templates for all letters
def everyFlag(img):
    upper = string.ascii_uppercase
    im = img
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    flag = ""
    
  
    for i in range(len(upper)):
        c = upper[i]
        
        p = path.absPath()
        f = p + "/Flags/" + c +".jpg"
        
        (im, hit) = matched(im, f)

        
        if hit:

            if c == "K" or c == "H":
                if isolateHotel(im):
                    flag = "H"
                else:
                    flag = "K"
                
            elif c == "S" or c == "I":
                if isolateIndia(im):
                    flag = "I"
                else:
                    flag = "S"

            elif c == "C" or c == "J":
                if isolateCharlie(im):
                    flag = "C"
                else:
                    flag = "J"
            else:
                flag = c
            
            break
            
    if len(flag) == 0:
        if isolateEcho(im):
            flag = "E"
               
    return (im, flag)
        
        
#compares image to given template
def matched(im, tm):
    hit = False
    img = im
    pts = []
    left = None
    top = None
    corners = []
    notCorner = False
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    template =  cv2.imread(tm,0)
    
    
    w,h = template.shape[1], template.shape[0]
    
    m = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    
    thresh = .8
    
    loc = np.where(m >= thresh)
    
    for point in zip(*loc[::-1]):

        if loc != None:
            hit = True
                
       
    return (img, hit)