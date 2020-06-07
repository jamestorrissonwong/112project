import path
import getImage

#used for keyboard
class key(object):
    
    def __init__(self, letter, x, y, size): 
        self.letter = letter.upper()
        self.x = x
        self.y = y
        self.size = size
        
        
        
    def checkInBounds(self, ex, ey):
        if (ex > self.x and ex < self.x+self.size) and (ey > self.y and ey < self.y+self.size):
            return True
        else: 
            return False
            
    def draw(self, canvas, data):
        canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill = "LightSteelBlue1")
        
        canvas.create_text(self.x + 0.5*self.size, self.y, anchor = "n", text = str(self.letter), font = ("Arial", (self.size//10)))
        

        
#creates a keyboard
def makeKeyboard(data, canvas, width, height, x0, y0):
    keyWidth = width//10
    keyHeight = width//3
    
    size = min(keyWidth, keyHeight)
    
    startWidth = x0 
    startHeight = y0 
    
    
    topRow = "QWERTYUIOP"
    midRow = "ASDFGHJKL"
    botRow = "ZXCVBNM"
    
    topKeys = []
    midKeys = []
    botKeys = []
    
    
    
    p = path.absPath()    
    

    for i in range(len(topRow)):
        letter = (topRow)[i]
        x = startWidth + size*i
        y = startHeight
        
       
        st = p + "/Flags/" + str(letter)  + ".jpg"
        data.imD[letter] = getImage.getIm(data, st, resize = True, sizeX = int(0.6 *size), sizeY = int(0.6*size))
        
        thisKey = key(letter, x, y, size)
        topKeys.append(thisKey)
        data.keys[letter] = thisKey
        thisKey.draw(canvas, data)
        im = data.imD[letter] 
        # print(x + 0.1*size, y + 0.1*size)
        canvas.create_image(x + 0.2*size, y + 0.2*size, anchor = "nw", image = im)
        
    for j in range(len(midRow)):
        letter = (midRow)[j]
        x = startWidth + size//3 + size*j
        y = startHeight + size
        
       
        st = p + "/Flags/" + str(letter)  + ".jpg"
        data.imD[letter] = getImage.getIm(data, st, resize = True, sizeX = int(0.6 *size), sizeY = int(0.6*size))
        

        thisKey = key(letter, x, y, size)
        midKeys.append(thisKey)
        data.keys[letter] = thisKey
        thisKey.draw(canvas, data)
        im = data.imD[letter] 
        canvas.create_image(x + 0.2*size, y + 0.2*size, anchor = "nw", image = im)
        
    
    for k in range(len(botRow)):
        letter = (botRow)[k]
        x = startWidth + 2*size//3 + size*k
        y = startHeight + 2*size
        

        st = p + "/Flags/" + str(letter)  + ".jpg"
        data.imD[letter] = getImage.getIm(data, st, resize = True, sizeX = int(0.6 *size), sizeY = int(0.6*size))
         
        
        thisKey = key(letter, x, y, size)
        botKeys.append(thisKey)
        data.keys[letter] = thisKey
        thisKey.draw(canvas, data)
        im = data.imD[letter] 
        canvas.create_image(x + 0.2*size, y + 0.2*size, anchor = "nw", image = im)