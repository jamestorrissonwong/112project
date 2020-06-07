from pathlib import Path
import os

def absPath():
    dir = os.path.realpath('..')

    filename = dir + "/FinalVersion"

    
    for i in range(len(filename)):
 
        if (filename[i] == '\\' ):
            filename = filename[0:i] + "/" + filename[i+1:]

    return filename