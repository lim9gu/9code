# Data processing Part with Flat

# For one day data.

import os
import sys
from pyraf import iraf
import numpy as np
import astropy.io.fits as fits
from iraf import imred, ccdred

# bias combine
os.chdir('bias')
os.system('ls *.fits > zero.list')
os.system('gethead *.fits FILTER OBJECT IMAGETYP EXPTIME')

def zerocom(im, op, comb, rej, ccdtype, scale, gain, rdnoise, mode) :
	print 'Combine Zero frames to Master-Zero...'
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

zerocom('@zero.list', 'zero', 'median', 'minmax', '', 'none', '1.2 ', '8.2 ', 'h' )
os.system('ds9 zero.fits -zoom to fit -single -match frame image &')
os.chdir('../')

# Master Dark 

os.chdir('dark')
os.system('ls *.fits > dark.list')
os.system('gethead *.fits FILTER OBJECT IMAGETYP EXPTIME')


def imarith(im, op, im2, result, mode):
	print 'Running imarith for input images...'
	iraf.module.imarith.setParam('operand1',im)
	iraf.module.imarith.setParam('op',op)
	iraf.module.imarith.setParam('operand2',im2)
	iraf.module.imarith.setParam('result',result)
	iraf.module.imarith.setParam('mode',mode)
	iraf.module.imarith()
	print 'Resultant file is '+str(result)
	
imarith('@dark.list', '-','../bias/zero.fits','z@dark.list','h')

def imcombine(im, op, comb, rej, scale,gain, rdnoise, mode):

	iraf.imcombine.setParam('input', im)
	iraf.imcombine.setParam('output', op)
	iraf.imcombine.setParam('combine', comb)
	iraf.imcombine.setParam('reject', rej)
	iraf.imcombine.setParam('scale', scale)
	iraf.imcombine.setParam('gain', gain)
	iraf.imcombine.setParam('rdnoise', rdnoise)
	iraf.imcombine.setParam('mode', mode)
	iraf.imcombine()
	print 'dark.fits is created.'
	
imcombine('z@dark.list', 'dark', 'median', 'minmax', 'none','1.2 ', '8.2 ','h')
os.system('ds9 dark.fits -zoom to fit -single -match frame image &')
os.chdir('../')
os.system('ds9 flat/2016*.fits -tile -zoom to fit -match frame image  &')
'''
def ccdproc(im, op, ccdtype, zerocor, darkcor, flatcor, mode ):
	
	iraf.noao.imred.ccdred()
	iraf.imred.unlearn()
	iraf.imred.ccdred.unlearn()
	iraf.imred.ccdred.ccdproc.unlearn()
	
	iraf.imred.ccdred.ccdproc.setParam('images', im)
	iraf.imred.ccdred.ccdproc.setParam('output', op)
	iraf.imred.ccdred.ccdproc.setParam('ccdtype', ccdtype)
	iraf.imred.ccdred.ccdproc.setParam('zerocor', zerocor)
	iraf.imred.ccdred.ccdproc.setParam('darkcor', darkcor)
	iraf.imred.ccdred.ccdproc.setParam('flatcor', flatcor)
	iraf.imred.ccdred.ccdproc.setParam('mode', mode)
	iraf.imred.ccdred.ccdproc()
ccdproc('', '', '', 'no','no','no','h')
'''

'''
def darkcom(im, op, comb, rej, ccdtype, scale, process, gain, rdnoise, mode) :
	print 'Combine dark frames to Master-Dark...'
	# Load packages
	iraf.imred.ccdred()

	# Unlearn settings
	iraf.imred.unlearn()
	iraf.imred.ccdproc.unlearn()
	iraf.imred.combine.unlearn()
	iraf.imred.darkcombine.unlearn()
	
	#setup task
	#ccdred.instrument = "ccddb$kpno/camera.dat"
	imred.darkcombine.setParam('input', im)
	imred.darkcombine.setParam('output', op)
	imred.darkcombine.setParam('combine', comb)
	imred.darkcombine.setParam('reject', rej)
	imred.darkcombine.setParam('ccdtype', ccdtype)
	imred.darkcombine.setParam('scale', scale)
	imred.darkcombine.setParam('process', process)
	imred.darkcombine.setParam('gain', gain)
	imred.darkcombine.setParam('rdnoise', rdnoise)
	imred.darkcombine.setParam('mode', mode)
	imred.darkcombine()
	print 'Resultant file is '+str(op)
	print 'Master-Dark frame is made.'

darkcom('@dark.list', 'dark', 'median', 'minmax', 'dark', 'none', 'no','', '', 'h' )





# Master Flat

os.chdir('flat')
os.system('ls *.fits > flat.list')
os.system('gethead *.fits  FILTER OBJECT IMAGETYP EXPTIME > fileinfo.txt')


files=np.genfromtxt('fileinfo.txt', usecols=(0,1), dtype=str)


iflats=[]
for image in files :
	I = np.where(image[0,1]== 'I')
	iflats.append(image[0,0])
ilist=open('iflat.fits','w')
ilist.close()

# hselect

def hselect(im, fields, expr,mode) :
	print 'Flat frames will be classified into each filter (hselect)...'
	
	iraf.module.hselect.unlearn()
	
	iraf.module.hselect.setParam('images', im)
	iraf.module.hselect.setParam('fields', fields)
	iraf.module.hselect.setParam('expr', expr)
	iraf.module.hselect.setParam('mode', mode)
	iraf.module.hselect()
	
fields='$I'
subexp="filter = 'I'"
expr= subexp + ' > iflat.list'








# $I "filter= 'I'" > iflat.list ; type iflat.list
hselect('@flat.list', fields,  expr)
hselect('@flat.list', '$I','\"filter= \'R\'\" > rflat.list ; type rflat.list' )
hselect('@flat.list', '$I','\"filter= \'R(Ha)\'\" > raflat.list ; type raflat.list' )
hselect('@flat.list', '$I','\"filter= \'V\'\" > vflat.list ; type vflat.list' )
hselect('@flat.list', '$I','\"filter= \'U\'\" > uflat.list ; type uflat.list' )
hselect('@flat.list', '$I','\"filter= \'B\'\" > bflat.list ; type bflat.list' )

# imstat

def imstat(im) :
	iraf.module()
	iraf.module.imstatistics.unlearn()

	iraf.module.imstatistics.setParam('images', im)
	iraf.module.imstatistics()
	
imstat('@flat.list')

def imarith(im, op, im2, result, mode):
	print 'Running imarith for input images...'
	iraf.module.imarith.setParam('operand1',im)
	iraf.module.imarith.setParam('op',op)
	iraf.module.imarith.setParam('operand2',im2)
	iraf.module.imarith.setParam('result',result)
	iraf.module.imarith.setParam('mode',mode)
	iraf.module.imarith()
	print 'Resultant file is '+str(result)
	
imarith('@flat.list', '-','../dark/dark.fits','dz@flat.list','h')

def flatcom(im, op, comb, rej, ccdtype, process, gain, rdnoise, scale, subset) :
	print 'Combine flat frames to Master-Flat...'
	# Load packages
	iraf.imred()
	iraf.ccdred()
	
	# Unlearn settings
	iraf.imred.unlearn()
	iraf.ccdred.unlearn()
	iraf.ccdred.ccdproc.unlearn()
	iraf.ccdred.combine.unlearn()
	iraf.ccdred.flatcombine.unlearn()
	
	#setup task
	iraf.ccdred.flatcombine.setParam('input', im)
	iraf.ccdred.flatcombine.setParam('output', op)
	iraf.ccdred.flatcombine.setParam('combine', 'median')
	iraf.ccdred.flatcombine.setParam('reject', 'minmax')
	iraf.ccdred.flatcombine.setParam('ccdtype', '')
	iraf.ccdred.flatcombine.setParam('process', process)
	iraf.ccdred.flatcombine.setParam('gain', '1.45')
	iraf.ccdred.flatcombine.setParam('rdnoise', '4.7')
	iraf.ccdred.flatcombine.setParam('scale', 'median')
	iraf.ccdred.flatcombine.setParam('subset', subset)
	iraf.ccdred.flatcombine()
	print 'Resultant file is '+str(op)
	print 'Master-Flat frame is made.'

flatcom('dz@uflat.list', 'uflat.fits', '-', '-')
flatcom('dz@bflat.list', 'bflat.fits', '-', '-')
flatcom('dz@vflat.list', 'vflat.fits', '-', '-')
flatcom('dz@rflat.list', 'rflat.fits', '-', '-')
flatcom('dz@iflat.list', 'iflat.fits', '-', '-')
flatcom('dz@raflat.list', 'raflat.fits', '-', '-')

imstat('*flat.fits')
os.system('ls *flat.fits > Flat.list')
flatlist=np.genfromtxt('flat.list',usecols=(0),dtype=str)
if 'bflat.fits' in flatlist : 
	bflat=fits.getdata('bflat.fits')
	bflath=fits.getheader('bflat.fits')
	mean_b=np.mean(bflat)
	nbflat=bflat - mean_b
	fits.writeto('nbflat.fits', nbflat, bflath ,clobber=True)

elif 'vflat.fits' in flatlist :
	vflat=fits.getdata('vflat.fits')
	vflath=fits.getheader('vflat.fits')
	mean_v=np.mean(vflat)
	nvflat=vflat - mean_v
	fits.writeto('nvflat.fits', nvflat, vflath ,clobber=True)

elif 'uflat.fits' in flatlist :
	uflat=fits.getdata('uflat.fits')
	uflath=fits.getheader('uflat.fits')
	mean_u=np.mean(uflat)
	nuflat=uflat - mean_u
	fits.writeto('nuflat.fits', nuflat, uflath ,clobber=True)

elif 'rflat.fits' in flatlist :
	rflat=fits.getdata('rflat.fits')
	rflath=fits.getheader('rflat.fits')
	mean_r=np.mean(rflat)
	nrflat=rflat - mean_r
	fits.writeto('nrflat.fits', nrflat, rflath ,clobber=True)

elif 'iflat.fits' in flatlist :
	iflat=fits.getdata('iflat.fits')
	iflath=fits.getheader('iflat.fits')
	mean_i=np.mean(iflat)
	niflat=iflat - mean_i
	fits.writeto('niflat.fits', niflat, iflath ,clobber=True)

elif '' in flatlist :
	print, 'There is no flat image !!! Check if it is error or not.'
	
imstat('n*flat.fits')
os.chdir('cd ../')

print('All Master Frames are created !!!')
os.system('ds9 n*flat.fits &')
'''

