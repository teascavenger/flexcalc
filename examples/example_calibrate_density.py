#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use Al dummy to callibrate density. Corrected reconstruction shoud show the density of aluminum = 2.7 g/cm3
"""
#%%
from flexdata import io
from flexdata import display

from flextomo import project

from flexcalc import process

import numpy

#%% Read

path = '/ufs/ciacc/flexbox/al_test/90KV_no_filt/'

dark = io.read_tiffs(path, 'di')
flat = io.read_tiffs(path, 'io')    
proj = io.read_tiffs(path, 'scan_')

meta = io.read_meta(path, 'flexray')   
 
#%% Prepro:
    
proj = (proj - dark) / (flat.mean(0) - dark)
proj = -numpy.log(proj)
proj = io.raw2astra(proj)    

proj = process.subtract_air(proj)

display.display_slice(proj, title = 'Sinogram')

#%% Reconstruct:
    
vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, title = 'Uncorrected FDK')
    
energy, spectrum = process.calibrate_spectrum(proj, vol,  meta['geometry'], compound = 'Al', density = 2.7, n_bin = 21, iterations = 1000)   

# Save:
numpy.savetxt(path + 'spectrum.txt', [energy, spectrum]) 

#%% Test:

proj_ = process.equivalent_density(proj,  meta['geometry'], energy, spectrum, compound = 'Al', density = 2.7) 

vol = project.init_volume(proj)
project.FDK(proj_, vol, meta['geometry'])

#vol /= meta['geometry']['img_pixel'] ** 4

display.display_slice(vol, title = 'Corrected FDK')

a,b = process.histogram(vol)
        
