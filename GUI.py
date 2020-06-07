from tkinter import *
from tkinter import filedialog
import string
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import string
import PIL
import tkinter
from PIL import Image, ImageTk
import os
import socket
import threading
from queue import Queue
import tkinter.font as tkfont
from pathlib import Path
import keyboard
import path
import getImage
import matching
import codes
import createIms

###
#Notes

#socket template used from https://kdchin.gitbooks.io/sockets-module-manual/

#color detection template from
#https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/

#run from https://www.cs.cmu.edu/~112/index.html
###

        

#hadndles incoming server messages    
def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  ship = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = " ".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")


#### GUI

def init(data):
    data.state = "Start"
    data.currFlags = ""
    data.currDef = ""
    data.codes = codes.codes()
    data.currPhoto = None
    data.image = None
    data.photoDef = ""
    data.photoFlags = []
    data.photoFlagsIms = []
    data.currIms = []
    data.chatPhoto = None
    data.chatFlags = []
    data.imD = {}
    data.keys = {}
    data.chatShift = 0
    data.saveFlags = []
    data.saveFlagsIms = []
    data.numYourIms = 0
    data.chatLog = []
    data.thisMsg = ""
    data.saveCurIm = None
    data.serverMsg = Queue(100)
    
    HOST = '127.0.0.1'
    PORT = 50003
    
    data.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    data.server.connect((HOST,PORT))
    print("connected to server")
    
    threading.Thread(target = handleServerMsg, args = (data.server, data.serverMsg)).start()

def mousePressed(event, data):
    x = event.x
    y = event.y
    
    ## Start
    if data.state == "Start":
        if (x > data.width//5) and (x < 2*data.width//5) and (y > 2*data.height//5) and (y < 3*data.height//5):
            data.state = "Photo"
        
        elif 3*x > data.width//5 and x < 4*data.width//5 and y > 2*data.height//5 and y < 3*data.height//5:
            data.state = "Definitions"
        
        elif (x > data.width//5) and (x < 2*data.width//5) and (y > 3.5*data.height//5) and (y < 4.5*data.height//5):
            data.state = "Chat"
            
        elif (x > 3*data.width//5) and (x < 4*data.width//5) and (y > 3.5*data.height//5) and (y < 4.5*data.height//5):
            data.state = "Save"
            
    ## Photo
    if data.state == "Photo":
    
        #Back
        if (x > 0) and (x < data.width//15) and (y > 0) and (y < data.height//15):
            data.state = "Start"
            data.currPhoto = None
            data.image = None
            data.photoDef = ""
            
        #Upload
        elif x > data.width//5 and x < 2*data.width//5 and y > 3*data.height//5 and y < 4*data.height//5:
            data.currPhoto  =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        
        #Decipher
        elif 3*x > data.width//5 and x < 4*data.width//5 and y > 3*data.height//5 and y < 4*data.height//5:
            
            data.photoFlags = matching.corners(data.currPhoto)
            #photoFlags is list of letters

            im = PIL.Image.open(data.currPhoto) 
            width, height = im.size
            
             
            newX = (data.width//5)
            newY = int(height*((data.width//5)/width))
            
        
            im = im.resize((newX,newY), PIL.Image.ANTIALIAS)
            data.ImObj = PIL.ImageTk.PhotoImage(im)
            

            result = (codes.getDefinition(data.photoFlags))
            data.photoDef = result[1]
            data.photoFlags = result[0]
            
            #gets templates of letters
            for c in data.photoFlags:
                p = path.absPath()
                st = p + "/Flags/" + c +".jpg"
                
                sqSize = min(data.width//5 , 7*data.height//30)
                thisIm = getImage.getIm(data, st, resize = True, sizeX = sqSize, sizeY = sqSize)
                
                data.photoFlagsIms.append(thisIm)
            
            data.state = "Deciphered"
            
    ## Definitions
    if data.state == "Definitions":

        #back
        if (x > 0) and (x < data.width//15) and (y > 0) and (y < data.height//15):
            data.state = "Start"
            data.currFlags = ""
            data.currDef = ""
            data.currIms = []
            
    ## Deciphered
    if data.state == "Deciphered":

        #back
        if (x > 0) and (x < data.width//15) and (y > 0) and (y < data.height//15):
            data.state = "Photo"
            data.currPhoto = None
            data.image = None
            data.photoDef = ""
            data.photoFlags = []
            data.photoFlagsIms = []
            
    
    ## Chat
    if data.state == "Chat":

        #back
        if (x > 0) and (x < data.width//15) and (y > 0) and (y < data.height//15):
            data.state = "Start"
            
        #upload
        elif (x > data.width//10) and (x < 3*data.width//10) and (y > 3*data.height//10) and (y < 4*data.height//10):
            data.chatPhoto = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            
            
            data.chatFlags = matching.corners(data.chatPhoto)
            
           
            im = PIL.Image.open(data.chatPhoto) 
            width, height = im.size
            
             
            newX = (data.width//5)
            newY = int(height*((data.width//5)/width))
            

            im = im.resize((newX,newY), PIL.Image.ANTIALIAS)
            
            data.ImObj = PIL.ImageTk.PhotoImage(im)
        
        
            result = (codes.getDefinition(data.chatFlags))
            data.photoDef = result[1]
            data.photoFlags = result[0]
            
            data.thisMsg += str(data.photoFlags)
            
        #keyboard
        for k in data.keys:
            thisKey = data.keys[k] 
            
            if thisKey.checkInBounds(x,y):
                data.thisMsg += str(k)

    ## Save
    if data.state == "Save":

        #back
        if (x > 0) and (x < data.width//15) and (y > 0) and (y < data.height//15):
            data.state = "Start"
            data.saveFlags = []
            data.saveFlagsIms = []

        #save
        elif (x > data.width//10) and (x < 2*data.width//10) and (y > 3*data.height//10) and (y < 4*data.height//10):
            singleIm = createIms.makeImage(data.saveFlagsIms)
            data.numYourIms += 1
            name = "YourFlag" + str(data.numYourIms)
            print("Saved " + name)
            createIms.saveIm(singleIm, name)

        #keyboard
        for k in data.keys:
            thisKey = data.keys[k] 
            
            if thisKey.checkInBounds(x,y):
                data.saveFlags += str(k)

        #combines flags into one image
        data.saveFlagsIms = []
        for i in range(len(data.saveFlags)):
            
            im = data.saveFlags[i]
            p = path.absPath()
            st = p + "/Flags/" + im + ".jpg"
            sqSize = min(data.width//5 , 7*data.height//30)
            img =  PIL.Image.open(st) 
            print("Im", img)
                        
            data.saveFlagsIms.append(img)


def keyPressed(event, data):

    
    if data.state == "Definitions":
        
        if event.keysym == "BackSpace":
            
            if(len(data.currIms)>0):

                if data.currFlags[-1] not in string.digits:
                    data.currIms.pop()

                data.currFlags = data.currFlags[0:-1]
            
            #in case there is no meaning for that set of flags
            try:
                data.currDef = (codes.getDefinition(data.currFlags))[1]
                
            except:
                data.currDef = ""

        elif event.keysym in string.ascii_letters or event.keysym in string.digits:
            

            if len(data.currFlags)<3:

                if event.keysym in string.digits and len(data.currFlags) < 2:
                    pass

                else:
                    c = (str(event.keysym)).upper()
                    data.currFlags += c
            

                if event.keysym in string.ascii_letters:
                    
                    sqSize = min(data.width//5 , 7*data.height//30)
                    
                    data.currIms = []
                    
                    for i in range(len(data.currFlags)):
                        im = data.currFlags[i]
                        p = path.absPath()
                        st = p + "/Flags/" + im + ".jpg"
                    
                        img = getImage.getIm(data, st, resize = True, sizeX = sqSize, sizeY = sqSize)
                        
                        data.currIms.append(img)
                        
                        
                data.currDef = (codes.getDefinition(data.currFlags))[1]
                    
                
        
                
    elif data.state == "Start":
        #shortcuts
        
        if event.keysym == "c":
             
            data.state = "Chat"

        elif event.keysym == "p":
             
            data.state = "Photo"

        elif event.keysym == "d":
             
            data.state = "Definitions"
             
        elif event.keysym == "s":

            data.state = "Save"
           

    elif data.state == "Chat":

    
        if event.keysym in string.ascii_letters:
            data.thisMsg = data.thisMsg + (event.keysym)
            
        elif event.keysym == "space":
            data.thisMsg = data.thisMsg + " "
            
        elif event.keysym == "BackSpace":
            data.thisMsg = data.thisMsg[0:-1]
        
        #send message
        elif event.keysym == "Return":
            
            if data.thisMsg != "":
                if data.thisMsg[-1] == " ":
                    data.thisMsg = data.thisMsg[0:-1]
                msg =  data.thisMsg + "\n"
                #print ("sending: ", msg)
                data.server.send(msg.encode())
                data.thisMsg = ""
        

    #Save
    elif data.state == "Save":

        if event.keysym in string.ascii_letters:
            letter = (str(event.keysym)).upper()
            data.saveFlags.append(letter)

        elif event.keysym == "BackSpace":
            data.saveFlags.pop()

        #combines flag images into one
        data.saveFlagsIms = []
        for i in range(len(data.saveFlags)):
            
            im = data.saveFlags[i]
            p = path.absPath()
            st = p + "/Flags/" + im + ".jpg"
            sqSize = min(data.width//5 , 7*data.height//30)
            img =  PIL.Image.open(st) 
            print("Im", img)
                        
            data.saveFlagsIms.append(img)


        

        

def timerFired(data):
    
   
                
    if data.state == "Chat":

        while (data.serverMsg.qsize() > 0):
            msg = data.serverMsg.get(False)
        

            
            parts = msg.split(" ")
            sendingShip = parts[0]
            shipMsg = parts[1:]
            
            if sendingShip == "myIDis":
                sendingShip = " "
                shipMsg = "Welcome to BoatChat " + str(shipMsg[0])
            
            data.chatLog.insert(0,[sendingShip, shipMsg])

            
            data.serverMsg.task_done()

def redrawAll(canvas, data):
    bgColor =  "PaleTurquoise1"
    butColor = "SteelBlue1"

    fs = [0, 0, data.width, data.height]
    top = [data.width//10, data.height//10, 9*data.width//10, 2*data.height//10]
    back = [0, 0, data.width//15, data.height//15]

    ##Start Screen
    if data.state == "Start":
        canvas.create_rectangle(fs, fill = bgColor)
        
        canvas.create_text(data.width//2, data.height//5, text = "International Code Flags", font = ("MS Serif", data.height//20, "bold"))
        
        #Photo Box
        canvas.create_rectangle(data.width//5, 2*data.height//5, 2*data.width//5, 3*data.height//5, fill = butColor)
        
        canvas.create_text(1.5*data.width//5, 2.5*data.height//5, text = "Photo", font = ("MS Serif", data.height//25))
    
        #Definition Box
        canvas.create_rectangle(3*data.width//5, 2*data.height//5, 4*data.width//5, 3*data.height//5, fill = butColor)
        
        canvas.create_text(3.5*data.width//5, 2.5*data.height//5, text = "Definitions", font = ("MS Serif", data.height//25))
    
        
        
        #Chat Box
        
        canvas.create_rectangle(data.width//5, 3.5*data.height//5, 2*data.width//5, 4.5*data.height//5, fill = butColor)
        
        canvas.create_text(1.5*data.width//5, 4*data.height//5, text = "Boat Chat", font = ("MS Serif", data.height//25))

        #Chat Box
        
        canvas.create_rectangle(3*data.width//5, 3.5*data.height//5, 4*data.width//5, 4.5*data.height//5, fill = butColor)
        
        canvas.create_text(3.5*data.width//5, 4*data.height//5, text = "Make Image", font = ("MS Serif", data.height//25))
        
        
    ##Photo Screen
    elif data.state == "Photo":
        canvas.create_rectangle(fs, fill = bgColor)
        
        canvas.create_text(data.width//2, data.height//5, text = "Upload a Photo and Decipher", font = ("MS Serif", data.height//20, "bold"))
        
        canvas.create_rectangle(back,fill = "White")
        
        canvas.create_text(0.5*data.width//15, 0.5*data.height//15, text = "Back", font = ("MS Serif", data.height//50))
        
        #Upload Box
        
        canvas.create_rectangle(data.width//5, 3*data.height//5, 2*data.width//5, 4*data.height//5, fill = butColor)
        
        canvas.create_text(1.5*data.width//5, 3.5*data.height//5, text = "Upload", font = ("MS Serif", data.height//20))
    
        #Decipher Box
        canvas.create_rectangle(3*data.width//5, 3*data.height//5, 4*data.width//5, 4*data.height//5, fill = butColor)
        
        canvas.create_text(3.5*data.width//5, 3.5*data.height//5, text = "Decipher", font = ("MS Serif", data.height//20))
    
    
    ## Definition Screen
    elif data.state == "Definitions":
        canvas.create_rectangle(fs, fill = bgColor)
        
        #Back
        canvas.create_rectangle(back, fill = "White")
        
        canvas.create_text(0.5*data.width//15, 0.5*data.height//15, text = "Back", font = ("MS Serif", data.height//50))
        
        
        #Side Screen
        canvas.create_rectangle(7*data.width//10, data.height//5, 9*data.width//10, 9*data.height//10,fill = "White")
        
        sqSize = min(data.width//5 , 7*data.height//30)
        for i in range(len(data.currIms)):
            im = data.currIms[i]
            
            canvas.create_image(7*data.width//10, data.height//5 + sqSize*i, anchor = "nw", image = im)

        #Text
        canvas.create_rectangle(top, fill = "White")
        
        canvas.create_text(data.width//10 + 10, data.height//10, text = str(data.currFlags), anchor = "nw", font = ("MS Serif", data.height//15))

        #Definition
        canvas.create_rectangle(data.width//10, 3*data.height//10, 6*data.width//10, 9*data.height//10, fill = "White")
        
        canvas.create_text(data.width//10 + 10, 3*data.height//10, text = str(data.currDef), anchor = "nw", width=data.width//2, font = ("MS Serif", data.height//25))
        
    ##Deciphered Screen
    elif data.state == "Deciphered":
        
        canvas.create_rectangle(fs, fill = bgColor)
        
        canvas.create_rectangle(back, fill = "White")
        
        canvas.create_text(0.5*data.width//15, 0.5*data.height//15, text = "Back", font = ("MS Serif", data.height//50))
        
        #Side Box
        canvas.create_rectangle(7*data.width//10, data.height//5, 9*data.width//10, 9*data.height//10,fill = "White")
        
        sqSize = min(data.width//5 , 7*data.height//30)
        
        for i in range(len(data.photoFlagsIms)):
            im = data.photoFlagsIms[i]
            canvas.create_image(7*data.width//10, data.height//5 + sqSize*i, anchor = "nw", image = im)
        
        #Top Box
        canvas.create_rectangle(top, fill = "White")
        
        #Side Box2
        canvas.create_rectangle(5*data.width//10, data.height//5, 7*data.width//10, 9*data.height//10,fill = "White")
        
        # im = ImageTk.PhotoImage(data.image)
        
        canvas.create_image(5*data.width//10, data.height//5, anchor = "nw", image = data.ImObj)
        
        #Def Box
        canvas.create_rectangle(data.width//10, 3*data.height//10, 5*data.width//10, 9*data.height//10, fill = "White")
        
        canvas.create_text(data.width//10 + 10, 3*data.height//10, text = str(data.photoDef), anchor = "nw", width=4*data.width//10, font = ("MS Serif", data.height//25))
        
        canvas.create_text(data.width//10 + 10, data.height//10, width=2*data.width//5, text = str(data.photoFlags), anchor = "nw", font = ("MS Serif", data.height//15))
        
        
    ##Chat Screen
    elif data.state == "Chat":
        canvas.create_rectangle(fs, fill = bgColor)
        
        canvas.create_rectangle(back, fill = "White")
        canvas.create_text(0.5*data.width//15, 0.5*data.height//15, text = "Back", font = ("MS Serif", data.height//50))
        
        #TopBox
        canvas.create_rectangle(top, fill = "White")
        
        canvas.create_text(data.width//10, data.height//10, anchor = "nw", font = ("MS Serif", 15), text = data.thisMsg, width = 8*data.width//10)
        
        
        #Chatlogs
        canvas.create_rectangle(5*data.width//10, data.height//5, 9*data.width//10, 9*data.height//10,fill = "White")
        
        #KeyBoard
        width = 4*data.width//10
        height = 4*data.height//10
        
        
        x0 = data.width//10 
        y0 = data.height//2
        
        keyboard.makeKeyboard(data, canvas, width, height, x0, y0)
        
        
        #text        
        cumHeight = 0
        
        for i in range(len(data.chatLog)):
            
            font = tkfont.Font(family="MS Serif", size=15, weight="normal")
            h = (tkfont.Font(font=["MS Serif"]).metrics("linespace"))
            m_len = (font.measure(data.chatLog[i]))
            
        
            cumHeight += math.ceil(m_len/(4*data.width//10))
            linesHeight = cumHeight * h
            
            if linesHeight < 7*data.height//10:
                canvas.create_text(6*data.width//10, (9/10)*data.height - cumHeight*1.5*10, text = data.chatLog[i][1], anchor = "w", width = 4*data.width//10, font = ("MS Serif", 15))
                
                canvas.create_text(data.width//2, (9/10)*data.height - cumHeight*1.5*10, text = data.chatLog[i][0], anchor = "w",  font = ("MS Serif", 15))
                
        #Upload
        canvas.create_rectangle(data.width//10, 3*data.height//10, 3*data.width//10, 4*data.height//10, fill = butColor)
        canvas.create_text(2*data.width//10, 3.5*data.height//10, text = "Upload Photo", font = ("MS Serif", 15))
            
    ## Save Screen
    elif data.state == "Save":

    
        data.saveCurIm = Image.new("RGB", (225, 225), color = (255,255,255))

        canvas.create_rectangle(fs, fill = bgColor)
        
        #Back
        canvas.create_rectangle(back, fill = "White")
        
        canvas.create_text(0.5*data.width//15, 0.5*data.height//15, text = "Back", font = ("MS Serif", data.height//50))
        
        
        #Side Screen
        canvas.create_rectangle(7*data.width//10, data.height//5, 9*data.width//10, 9*data.height//10,fill = "White")
        

        if len(data.saveFlagsIms) != 0:
            data.saveCurIm = createIms.makeImage(data.saveFlagsIms)

            x, y = data.saveCurIm.size
            base = max((x/(2*data.width//10)), (y/(7*data.height//10)))
           
            data.saveCurIm = data.saveCurIm.resize( (int(x / base), int(y / base)), PIL.Image.ANTIALIAS)

            data.saveCurIm = PIL.ImageTk.PhotoImage(data.saveCurIm)

            canvas.create_image(7*data.width//10, data.height//5, anchor = "nw", image = data.saveCurIm)

        #Text
        canvas.create_rectangle(top, fill = "White")
        
        st = ""
        for i in data.saveFlags:
            st += i

        canvas.create_text(data.width//10 + 10, data.height//10, text = st, anchor = "nw", font = ("MS Serif", data.height//15))

        #Save
        canvas.create_rectangle(data.width//10, 3*data.height//10, 2*data.width//10, 4*data.height//10, fill = "White")
        
        canvas.create_text(data.width//10 + 10, 3*data.height//10, text = "Save", anchor = "nw", width=data.width//2, font = ("MS Serif", data.height//25))

        #Keyboard
        width = 4*data.width//10
        height = 4*data.height//10
        
        
        x0 = data.width//10 
        y0 = data.height//2
        
        keyboard.makeKeyboard(data, canvas, width, height, x0, y0)

#### Run
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1600, 800)