cd UGC04056
!gethead 2016*.fits FILTER OBJECT IMAGETYP EXPTIME
ls 2016*.fits > obj.list

imarith @obj.list - ../bias/zero.fits z@obj.list
imarith z@obj.list - ../dark/dark.fits dz@obj.list


hselect dz@obj.list $I "filter='R'" > robj.list ; type robj.list
hselect dz@obj.list $I "filter='I'" > iobj.list ; type iobj.list



imarith @iobj.list / ../flat/niflat.fits f@iobj.list
imarith @robj.list / ../flat/nrflat.fits f@robj.list


!ds9 fdz*.fits &
ls fdz*.fits > all.list
