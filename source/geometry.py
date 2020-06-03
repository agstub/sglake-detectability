#-------------------------------------------------------------------------------
# This file defines the bed topography and initial ice-water interface functions.
# Note: Bed and ice-water interface should be equal on margins of the domain!
#-------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from params import Lngth,Hght,tol,X_fine,nx

def bed(x):
    # generate bed topography
    B = -7*(np.exp((-(x-Lngth/2.0)**2)/((0.01*4*Lngth)**2) )) + 3.5
    return B

def interface(x):
    # generate initial ice-water/ice-bed interface
    Int = np.maximum(0*x,bed(x))
    return Int