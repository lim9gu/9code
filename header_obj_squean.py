# Code for finding fits files using header query [SQUEAN]
# G.Lim 2017-02-09

import os, sys
import numpy as np
from astropy.io import fits

folder = str(sys.argv[1]) # directory name YYYYMMDD or GRBXXXXXXA.
object = str(sys.argv[2]) # Enter object name which you are looking for. Try other names like M51, M51a, Messier51, messier51...

os.chdir(folder)
os.system('ls *.fits > inim.list')

inim = np.genfromtxt('inim.list', dtype = str)

for i = 0 in range(len(inim)) :
  
