import PIL
from PIL import Image
import path

#joins individual flag images into one
def makeImage(lst):


    if len(lst) == 0:
        pass
    else:
 
        numFlags = len(lst)
        margin = 50
        size = 225
        between = 20

        allFlagsImage = Image.new("RGB", (size + margin, (size+between)*numFlags + margin), color = "white")

  
        for i in range(len(lst)):
            thisFlagIm = lst[i]

            x, y = int(margin//2), int(margin//2+ i*(size+between))
            allFlagsImage.paste(thisFlagIm, (x, y, x+size, y+size))

        return allFlagsImage

#saves an image file
def saveIm(image, name):
    p = path.absPath()

    st = p + "/myFlags/" + name + ".jpg"
    
    image.save(st)

