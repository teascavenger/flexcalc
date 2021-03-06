#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test finding the rotation centre example.
"""
#%% Imports:
from flexdata import display

from flextomo import project

from flexcalc import process

#%% Read

path = '/ufs/ciacc/flexbox/al_test/90KV_no_filt/'

proj, meta = process.process_flex(path)

#%% Use optimize_rotation_center:
    
guess = process.optimize_rotation_center(proj, meta['geometry'], subscale = 8)

#%% Reconstruct uncorrected:

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, bounds = [], title = 'FDK Corrected')

#%% REconstruct corrected:

meta['geometry']['axs_hrz'] = guess

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, bounds = [], title = 'FDK Corrected')
