# Code for finding fits files using header query [SQUEAN]
# G.Lim 2017-02-09

import os, sys
import numpy as np
from astropy.io import fits

folder = str(sys.argv[1]) # directory name YYYYMMDD or GRBXXXXXXA.
header_name = str(sys.argv[2]) # Choose in object, filter, exptime, imagetype.
input = str(sys.argv[3]) # input header name which you are looking for. 

# object : Try other names like M51, M51a, Messier51, messier51...
# filter : U, B, V, R, I , u, g, r, i, z ...
# imagetype : bias, object, flat...

os.chdir(folder)
os.system('ls *.fits > inim.list')

inim = np.genfromtxt('inim.list', dtype = str)

object = []
filter = []
exptime = []
imagetype = []

for i = 0 in range(len(inim)) :
  hdr = fits.getheader(inim[i])
  
  obj = hdr['object']
  fil = hdr['filter']
  expt = hdr['exptime']
  imtype = hdr['imagetype']
  if header_name == object
    if input == obj :
  if header_name == filter
    if input == fil :
  if header_name == exptime
    if input == fil :
  if header_name == imagetype
    if input == fil :
      
      
      
      
      
      
      
      
      
      
      
