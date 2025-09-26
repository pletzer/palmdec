import vtk
import xarray as xr
import numpy as np

class Reader:
    
    def __init__(self, filename):
        
        # Read the file
        self.ds = xr.open_dataset(filename)
        
        x, y, z = self.ds['xu'], self.ds['yv'], self.ds['zw_3d']
        self.time = self.ds['time']
        
        # Assume equal spacing, all axes are monotonically increasing
        hx, hy, hz = x[1] - x[0], y[1] - y[0], z[1] - z[0]
        
        # Number of points = number of cells + 1
        nx = len(x)
        ny = len(y)
        nz = len(z)
        nt = len(self.time)
        nx1 = nx + 1
        ny1 = ny + 1
        nz1 = nz + 1
        nt1 = nt + 1
        
        # Build the grid
        self.grid = vtk.vtkUniformGrid()
        self.grid.SetDimensions(nx1, ny1, nz1)
        
        xmin, ymin, zmin = x[0], y[0], z[0]
        self.grid.SetOrigin(xmin, ymin, zmin)
        self.grid.SetSpacing(hx, hy, hz)
        
        # Add the face centred velocity data
        u2 = vtk.vtkFloatArray()
        u2.SetNumberOfComponents(1)
        # Attach to cells
        u2.SetNumberOfTuples(nz * ny * nx)
        u2.SetName("u2")
        
        # Add to cells
        self.grid.GetCellData().AddArray(u2)

    
    def getVtkGrid(self):
        return self.grid
    