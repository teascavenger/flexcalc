#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test finding the detector tilt example.
"""
#%% Imports:

import numpy

from flexdata import display

from flextomo import project

from flexcalc import process

#%% Read

path = '/ufs/ciacc/flexbox/al_test/90KV_no_filt/'

proj, meta = process.process_flex(path, sample = 2, skip = 2)

#%% Use optimize_rotation_center:

# Name and range of the parameter to optimize:
key = 'det_rot'
trial_values = numpy.linspace(-1, 1, 20)

# Subsampling of data (vertical x 10)
samp = [10, 1, 1]

# Optimization:
guess = process.optimize_modifier_subsample(trial_values, proj, meta['geometry'], samp = samp, key = key, preview = True)

#%% Reconstruct uncorrected:

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, bounds = [], title = 'FDK Corrected')

#%% REconstruct corrected:

meta['geometry'][key] = guess

vol = project.init_volume(proj)
project.FDK(proj, vol, meta['geometry'])

display.display_slice(vol, bounds = [], title = 'FDK Corrected')
