# Code for finding fits files using header query [SQUEAN]
# G.Lim 2017-02-09

import os, sys
import numpy as np
from astropy.io import fits

folder = str(sys.argv[1]) # directory name YYYYMMDD or GRBXXXXXXA.
header_name = str(sys.argv[2]) # Choose in object, filter, exptime, imagetype.
object = str(sys.argv[3]) # Enter header name which you are looking for. 

# object : Try other names like M51, M51a, Messier51, messier51...
# filter : U, B, V, R, I , u, g, r, i, z ...
# exptime 

os.chdir(folder)
os.system('ls *.fits > inim.list')

inim = np.genfromtxt('inim.list', dtype = str)

for i = 0 in range(len(inim)) :
  hdr = fits.getheader(inim[i])
  objname = hdr['object']
  filter = hdr['filter']
  exptime = hdr['exptime']
  imagetype = hdr['']
