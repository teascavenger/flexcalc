#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test finding rotation routine.
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

display.display_slice(proj, title = 'Sinogram')

#%% Use optimize_rotation_center:
    
guess = process.optimize_rotation_center(proj, meta['geometry'], guess = 0, subscale = 8)

#%% Recon
meta['geometry']['axs_hrz'] = guess

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, bounds = [], title = 'FDK')


#%%


