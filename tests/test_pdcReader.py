from importlib import resources
from palmdec import pdcReader

def test_reader():
    with resources.path("palmdec.data", "DATA_3D_NETCDF") as filename:
        rd = pdcReader.Reader(filename)
