import PIL
import tkinter
from PIL import Image, ImageTk

#opens image pathway and converts for tkinter compatibility
def getIm(data, str, resize = False, sizeX = None, sizeY = None):
    im = PIL.Image.open(str) 
    
    if resize:
        im = im.resize((sizeX,sizeY), PIL.Image.ANTIALIAS)
    
    image = PIL.ImageTk.PhotoImage(im)
    
    return image
    