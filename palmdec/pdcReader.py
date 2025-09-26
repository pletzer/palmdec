import vtk
import xarray as xr
import numpy as np

class Reader:
    
    def __init__(self, filename):
        
        # Read the file
        ds = xr.open_dataset(filename)
        
        x, y, z = ds['xu'], ds['yv'], ds['zw_3d']
        time = ds['time']
        
        # Assume equal spacing, all axes are positively increasing
        hx, hy, hz = x[1] - x[0], y[1] - y[0], z[1] - z[0]
        
        # Number of points = number of cells + 1
        nx = len(x)
        ny = len(y)
        nz = len(z)
        nt = len(time)
        nx1 = nx + 1
        ny1 = ny + 1
        nz1 = nz + 1
        nt1 = nt + 1
        
        # Build the grid
        self.grid = vtk.vtkUniformGrid()
        self.grid.SetDimensions(nx1, ny1, nz1)
        
        xmin, xmax = x[0], x[-1] + hx
        ymin, ymax = y[0], y[-1] + hy
        zmin, zmax = z[0], z[-1] + hz
        self.grid.SetExtents(xmin, xmax, ymin, ymax, zmin, zmax)
        
        # Add the face centred velocity data
        u2 = vtk.vtkFloatArray()
        u2.SetNumberOfComponents(1)
        # Attach to cells
        u2.SetNumberOfTuples(nz, ny, nx)
        u2.SetName("u2")
        
        # Add to cells
        self.grid.GetCellData().AddArray(u2)

    
    def getVtkGrid(self):
        return self.grid
    