import picamera
import picamera.array
from time import localtime, strftime
from datetime import datetime
import numpy as np
import time
from PIL import Image #Image splicing

from funcs import *
rows=128
cols=128

n_pics=2

#Take picture
with picamera.PiCamera() as camera:
    camera.resolution = (rows, cols)
    camera.framerate = 24
    camera.start_preview()
    time.sleep(2)
    output1 = np.empty((rows, cols, 3), dtype=np.uint8)
    output2 = np.empty((rows, cols, 3), dtype=np.uint8)
    camera.capture(output1, 'rgb') # Get array
    print("Move to position 2, then hit enter")
    input()
    camera.capture(output2, 'rgb') # Get array
    camera.capture('capture1.jpg') # Make image
    camera.capture('capture2.jpg') # Make image
    
    output = np.empty((rows, cols*2, 3), dtype=np.uint8)
    output[:,:cols,:]=output1
    output[:,cols:,:]=output2

    image = Image.fromarray(output.astype('uint8')).convert('RGB')
    image.save('splice.jpg')

file_path="output.txt"
# Open the file for writing
with open(file_path, 'w') as f:
    # Write the shape of the array as the first line
    f.write(','.join(map(str, output.shape)) + '\n')

    # Write each element of the array
    for matrix in output:
        for row in matrix:
            # Write each row of the matrix, separated by commas
            f.write(' '.join(map(str, row)))
            f.write(',')
        f.write('\n')
    
#Convert to black and white
black_and_white = np.empty((rows, cols), dtype=np.uint8)
for r in range(rows):
    for c in range(cols):
        black_and_white[r, c]=.3*output[r,c,0]+.59*output[r,c,1]+.11*output[r,c,2]
        print(black_and_white[r,c] ,end= ' ')
    print()


print('_'*cols)
for r in range(rows):
    for c in range(cols):
        if (black_and_white[r, c] <  100):
            print('.' ,end='')
        else:
            print(' ',end='')
    print('|')

print('_'*cols)


