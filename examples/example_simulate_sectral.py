#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate spectral data with Poisson noise.
"""
#%% Imports

from flexdata import io
from flexdata import display

from flextomo import project
from flextomo import phantom

from flexcalc import spectrum
from flexcalc import process

import numpy
   
#%% Define a simple projection geometry:
geometry = io.init_geometry(src2obj = 100, det2obj = 100, det_pixel = 0.2, 
                            theta_range = [0, 360], geom_type = 'simple')

#%% Short version:
vol = phantom.cuboid([1,128,128], geometry, 8,8,8)  
display.display_slice(vol , title = 'Phantom') 

# Spectrum:    
E, S = spectrum.effective_spectrum(kv = 90)  
display.plot(E,S, title ='Spectrum')   
  
mats = [{'material':'Al', 'density':2.7},]
                
counts = numpy.zeros([1, 128, 128], dtype = 'float32')

# Simulate:
spectrum.forward_spectral(vol, counts, geometry, mats, E, S, n_phot = 1e6)

# Display:
display.display_slice(counts, title = 'Modelled sinogram')  

#%% Reconstruct:
    
vol_rec = numpy.zeros_like(vol)
proj = -numpy.log(counts)

project.FDK(proj, vol_rec, geometry)
display.display_slice(vol_rec, title = 'Uncorrected FDK')
display.plot(vol_rec[0, 64])       

#%% Correct Beam Hardening:

# Make a fake meta record:
meta = io.init_meta(geometry)

# Compute the spectrum:
energy, spectrum = process.calibrate_spectrum(proj, vol, 
                                              meta, compound = 'Al', density = 2.7, iterations = 1000, n_bin = 20) 

# Correct data:
proj = process.equivalent_density(proj,  meta, energy, spectrum, compound = 'Al', density = 2.7)

# Reconstruct:
vol_rec = numpy.zeros_like(vol)
project.FDK(proj, vol_rec, geometry)

# Display:
display.display_slice(vol_rec, title = 'Corrected FDK')
display.plot(vol_rec[0, 64])      