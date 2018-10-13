#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load a standard CT scan. Reconstruct using different methods.
"""
#%%from flexdata import io
from flexdata import display
from flextomo import project

from flexcalc import process

import numpy

#%% Read and process:

path = '/ufs/ciacc/flexbox/al_test/90KV_no_filt/' 
proj, meta = process.process_flex(path) 

#%% FDK Recon

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])
display.display_slice(vol, bounds = [], title = 'FDK')

#%% EM

vol = numpy.ones([10, 2000, 2000], dtype = 'float32')
project.EM(proj, vol, meta['geometry'], iterations = 3)
display.display_slice(vol, title = 'EM')

#%% SIRT with additional options

vol = numpy.zeros([1, 2000, 2000], dtype = 'float32')

options = {'bounds':[0, 1000], 'l2_update':True, 'block_number':3, 'mode':'sequential'}
project.SIRT(proj, vol, meta['geometry'], iterations = 3, options = options)
display.display_slice(vol, title = 'SIRT')