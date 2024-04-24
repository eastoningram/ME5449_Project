import picamera
import picamera.array
from time import localtime, strftime
from datetime import datetime
import numpy as np
import time
from PIL import Image #Image splicing
import RPi.GPIO as GPIO
from rdp import rdp # Ramer-Douglas-Peucker Algorithm
import matplotlib.pyplot as plt # graphing tool

from funcs import *
rows=128
cols=128

x_frames=2
y_frames=2

GPIO.setmode(GPIO.BCM)
switch=26 # Input from robot
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


frame = np.empty((rows, cols, 3), dtype=np.uint8)
frame0 = np.empty((rows, cols, 3), dtype=np.uint8)
output = np.empty((rows*x_frames, cols*y_frames, 3), dtype=np.uint8)

#Take picture
with picamera.PiCamera() as camera:
    camera.resolution = (rows, cols)
    camera.framerate = 24

    for j in range(y_frames):
        for i in range(x_frames):
            print(GPIO.input(switch))
            # wait for input from robot
            while not GPIO.input(switch):
                time.sleep(0.01)
            
            camera.capture(frame0, 'rgb') # Grab array
            frame=np.rot90(frame0)
            output[j*rows:(j+1)*rows,i*cols:(1+i)*cols,:]=frame # Splice images together
            camera.capture('capture_'+str(i) + '_' + str(j) + '.jpg') # Make image
            print('Took x= ' +str(i)+', y= '+ str(j))
            while GPIO.input(switch):
                time.sleep(0.01)
    
    image = Image.fromarray(output.astype('uint8')).convert('RGB')
    image.save('splice.jpg')

GPIO.cleanup()

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
#for r in range(rows):
 #   for c in range(cols):
  #      black_and_white[r, c]=.3*output[r,c,0]+.59*output[r,c,1]+.11*output[r,c,2]
   #     print(black_and_white[r,c] ,end= ' ')
    #print()

points=[(0,0)]*rows*cols
n_points=0

#print('_'*cols)
for r in range(rows):
    for c in range(cols):
        if (black_and_white[r, c] <  100):
      #      print('.' ,end='')
            points[n_points]=[c,r]
            n_points=n_points+1
        #else:
            #print(' ',end='')
    #print('|')

#print('_'*cols)

"""

# Extract x and y coordinates from the points
x_values = [point[0] for point in points]
y_values = [point[1] for point in points]

# Plot the points
plt.scatter(x_values, y_values)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of Points')
plt.grid(True)
plt.show()

new_points=rdp(points,.3)

# Extract x and y coordinates from the points
new_x_values = [point[0] for point in new_points]
new_y_values = [point[1] for point in new_points]

# Plot the points
plt.scatter(new_x_values, new_y_values)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of Points')
plt.grid(True)
plt.show()
"""

