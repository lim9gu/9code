# Code for running gresister IRAF to Maidanak.
# Correct the distortion of WCS coordinate.
# 2017-08-13 G.Lim created.

from pyraf import iraf
import numpy as np
import os, sys

'''
gregister input output database transforms

(input)
List of images to be transformed.

(output)
List of output images.

(database)
The name of the text file database produced by GEOMAP 
containing the coordinate transformation(s).

(transforms)
The list of the database record(s) containing the transformations. 
The number of transforms must be 1 or the same as the number of input images. 
Transforms is usually the name of the text file input to GEOMAP 
which lists the reference and input coordinates of the control points.
'''
os.system('ls ac*.fits > im.list')

iraf.gregister('input=@im.list output=g@im.list database= ')



os.system('rm im.list')
