#20170207/flat/flat1/bias/

import os
import sys
from pyraf import iraf
import numpy as np
import astropy.io.fits as fits
from iraf import imred, ccdred

def zerocom(im, op, comb, rej, ccdtype, scale, gain, rdnoise, mode) :
	print 'Combine Zero frames to Master-Zero...'
  ccdred.instrument = "ccddb$kpno/camera.dat"
	# Load packages
	iraf.imred()
	iraf.ccdred()
	
	# Unlearn settings
	iraf.imred.unlearn()
	iraf.ccdred.unlearn()
	iraf.ccdred.ccdproc.unlearn()
	iraf.ccdred.combine.unlearn()
	iraf.ccdred.zerocombine.unlearn()
	
	#setup task
	iraf.ccdred.zerocombine.setParam('input', im)
	iraf.ccdred.zerocombine.setParam('output', op)
	iraf.ccdred.zerocombine.setParam('combine', comb)
	iraf.ccdred.zerocombine.setParam('reject', rej)
	iraf.ccdred.zerocombine.setParam('ccdtype', ccdtype)
	iraf.ccdred.zerocombine.setParam('scale', scale)
	iraf.ccdred.zerocombine.setParam('gain', gain)
	iraf.ccdred.zerocombine.setParam('rdnoise', rdnoise)
	iraf.ccdred.zerocombine.setParam('mode', mode)
	iraf.ccdred.zerocombine()
	print 'Resultant file is '+str(op)
	print 'Master-Zero frame is made.'

os.chdir('flat')

# bias combine in flat1
os.chdir('bias')
os.system('ls *.fits > zero.list')
zerocom('@zero.list', 'zero', 'median', 'crreject', '', 'none', '1.2 ', '8.2 ', 'h' )
#os.system('ds9 zero.fits -zoom to fit -single -match frame image &')

def imarith(im, op, im2, result, mode):
	print 'Running imarith for input images...'
	iraf.module.imarith.setParam('operand1',im)
	iraf.module.imarith.setParam('op',op)
	iraf.module.imarith.setParam('operand2',im2)
	iraf.module.imarith.setParam('result',result)
	iraf.module.imarith.setParam('mode',mode)
	iraf.module.imarith()
	print 'Resultant file is '+str(result)

os.chdir('../')


# bias combine in flat2

os.chdir('bias')
os.system('ls *.fits > zero.list')
zerocom('@zero.list', 'zero', 'median', 'crreject', '', 'none', '1.2 ', '8.2 ', 'h' )
os.system('ds9 zero.fits -zoom to fit -single -match frame image &')
os.chdir('../')

