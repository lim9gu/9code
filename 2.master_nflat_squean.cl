cd flat

noao
imred
ccdred

ls 2016*.fits > allflat.list
hselect @allflat.list $I "object= 'Skyflat'" > flat.list ; type flat.list
imstat @flat.list

imarith @flat.list - ../bias/zero.fits z@flat.list
imstat z@flat.list

hselect z@flat.list $I "filter= 'I'" > iflat.list ; type iflat.list
hselect z@flat.list $I "filter= 'R'" > rflat.list ; type rflat.list


flatcombine @rflat.list output=rflat.fits combine=median reject=minmax ccdtype='' process- gain=1.2 rdnoise=8.2 scale=mode subset-
flatcombine @iflat.list output=iflat.fits combine=median reject=minmax ccdtype='' process- gain=1.2 rdnoise=8.2 scale=mode subset-

imstat rflat.fits field='mean' format- | scan(x)
=x
imarith rflat.fits / (x) nrflat.fits

imstat iflat.fits field='mean' format- | scan(x)
=x
imarith iflat.fits / (x) niflat.fits

imstat n*flat.fits
!ds9 n*flat.fits &
cd ..
ls

