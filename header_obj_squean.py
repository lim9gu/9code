# Code for finding fits files using header query [SQUEAN]
# G.Lim 2017-02-09

import os, sys
import numpy as np
from astropy.io import fits

folder = str(sys.argv[1]) # directory name YYYYMMDD or GRBXXXXXXA.
header_name = str(sys.argv[2]) # Choose in object, filter, exptime, imagetype.
input = str(sys.argv[3]) # input header name which you are looking for. 

#FUTURE WORK
#operand1 = str(sys.argv[4]) # and, or
#input2 = str(sys.argv[5]) # 2nd header name which you are looking for.

# object : Try other names like M51, M51a, Messier51, messier51...
# filter : U, B, V, R, I , u, g, r, i, z ...
# imagetype : bias, object, flat...

os.chdir(folder)
os.system('ls *.fits > inim.list')

inim = np.genfromtxt('inim.list', dtype = str)

im_list = []
object_list = []
filter_list = []
exptime_list = []
imagetype_list = []

for i = 0 in range(len(inim)) :
  hdr = fits.getheader(inim[i])
  
  obj = hdr['object']
  fil = hdr['filter']
  expt = hdr['exptime']
  imtype = hdr['imagetype']
  
  if header_name == 'object'
    if input == obj :
      print str(inim[i])
      print 'Input : '+input+', Header :'+str(obj)
      im_list.append(inim[i])
      object_list.append(obj)
    else :
      continue

  if header_name == 'filter'
    if input == fil :
      print str(inim[i])
      print 'Input : '+input+', Header :'+str(fil)
      im_list.append(inim[i])
      filter_list.append(fil)
    else :
      continue
  
  if header_name == 'exptime'
    if input == expt :
      print str(inim[i])
      print 'Input : '+input+', Header :'+str(expt)
      im_list.append(inim[i])
      exptime_list.append(expt)
    else :
      continue
  
  if header_name == 'imagetype'
    if input == imtype :
      print str(inim[i])
      print 'Input : '+input+', Header :'+str(imtype)
      im_list.append(inim[i])
      imagetype_list.append(imtype)
    else :
      continue

if header_name == 'object' :
  print im_list, object.list 
if header_name == 'filter' :
  print im_list, filter.list 
if header_name == 'exptime'
  print im_list, exptime.list 
if header_name == 'imagetype'
  print im_list, imagetype.list 
            
os.system('rm inim.list')      
os.chdir('../')           

print 'Done.'
      
      
      
      
      
      
      
