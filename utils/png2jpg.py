import cv2
import os
from glob import glob

pngs = glob('./images/*.png')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'jpg', img)
    os.remove(j)
