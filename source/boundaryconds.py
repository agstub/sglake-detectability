#-------------------------------------------------------------------------------
# This file contains functions that:
# (1) define the boundaries (ice-air,ice-water,ice-bed) of the mesh,
# (2) mark the boundaries of the mesh, AND...
# (3) create the Dirichlet boundary conditions
#-------------------------------------------------------------------------------
from params import tol,Lngth,Hght,wall_bcs
from geometry import bed
import numpy as np
from dolfin import *

#-------------------------------------------------------------------------------
# Define SubDomains for ice-water boundary, ice-bed boundary, inflow (x=0) and
# outflow (x=Length of domain). The parameter 'tol' is a minimal water depth
# used to distinguish the ice-water and ice-bed surfaces.

class WaterBoundary(SubDomain):
    # Ice-water boundary.
    # This boundary is marked first and all of the irrelevant portions are
    # overwritten by the other boundary markers.
    def inside(self, x, on_boundary):
        return (on_boundary and (x[1]<0.5*Hght))

class BedBoundary(SubDomain):
    # Ice-bed boundary
    def inside(self, x, on_boundary):
        return (on_boundary and ((x[1]-bed(x[0]))<=tol))

class LeftBoundary(SubDomain):
    # Left boundary
    def inside(self, x, on_boundary):
        return (on_boundary and np.abs(x[0])<tol)

class RightBoundary(SubDomain):
    # Right boundary
    def inside(self, x, on_boundary):
        return (on_boundary and np.abs(x[0]-Lngth)<tol)

#-------------------------------------------------------------------------------

def mark_boundary(mesh):
    # Assign markers to each boundary segment (except the upper surface).
    # This is used at each time step to update the markers.
    #
    # Boundary marker numbering convention:
    # 1 - Left boundary
    # 2 - Right boundary
    # 3 - Ice-bed boundary
    # 4 - Ice-water boundary
    #
    # This function returns these markers, which are used to define the
    # boundary integrals and dirichlet conditions.

    boundary_markers = MeshFunction('size_t', mesh,dim=1)
    boundary_markers.set_all(0)

    # Mark ice-water boundary
    bdryWater = WaterBoundary()
    bdryWater.mark(boundary_markers, 4)

    # Mark ice-bed boundary
    bdryBed = BedBoundary()
    bdryBed.mark(boundary_markers, 3)

    # Mark inflow boundary
    bdryLeft = LeftBoundary()
    bdryLeft.mark(boundary_markers, 1)

    # Mark outflow boundary
    bdryRight = RightBoundary()
    bdryRight.mark(boundary_markers, 2)

    return boundary_markers

#------------------------------------------------------------------------------

def create_dir_bcs(W,boundary_markers):
    # Apply inflow and outflow boundary conditions to the system.
    # These are applied to the horizontal velocity component.

    # dirichlet conditions: apply zero inflow/outflow velocity
    if wall_bcs == 'dirichlet':
        bcu1 = DirichletBC(W.sub(0).sub(0), Constant(0.0), boundary_markers,1)
        bcu2 = DirichletBC(W.sub(0).sub(0), Constant(0.0), boundary_markers,2)
        bcs = [bcu1,bcu2]

    # neumann conditions: return empty array of dirichlet conditions
    elif wall_bcs == 'neumann':
        bcs = []

    return bcs