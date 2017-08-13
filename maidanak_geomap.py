from pyraf import iraf
import os, sys
import numpy as np

'''
geomap input database xmin xmax ymin ymax

(input)
The list of text files containing the pixel coordinates of control points in the reference and input images. 
The control points are listed one per line with xref, yref, xin, and yin in columns 1 through 4 respectively.

(database)
The name of the text file database 
where the computed transformations will be stored.

(xmin, xmax, ymin, ymax)
The range of reference coordinates over 
which the computed coordinate transformation is valid. 
If the user is working in pixel units, 
these limits should normally be set to the values of the column and row limits of the reference image, 
e.g xmin = 1.0, xmax = 512, ymin= 1.0, ymax = 512 for a 512 x 512 image. 
The minimum and maximum xref and yref values in input are used if xmin, xmax, ymin, or ymax are undefined.
'''
os.system('ls ac*.fits > im.list')

# Input list
print 'Create the input list file...'

xref = str(sys.argv[1])
yref = str(sys.argv[2])
xin = str(sys.argv[3])
yin = str(sys.argv[4])

f=open('coor.txt','w')

f.write(xref)
f.write(yref)
f.write(xin)
f.write(yin)

f.close()
print 'Finish the input list file.'

print 'Run geomap...'
iraf.geomap(input = @im.list database = gregister.geo)

os.system('rm im.list')
print 'Done.'






