
#작성자: 이준영
#작성일: 2019_11_15

import vtk
from vtk.util import numpy_support
import os
import numpy
from matplotlib import pyplot, cm
import scipy.ndimage.interpolation as ndinter

PathDicom = 'C:/Users/HH211/Desktop/BNCT_TEMP_20190812/CT_Image'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()

# Load dimensions using 'GetDataExtent'
_extent = reader.GetDataExtent()
ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]

# Load spacing values
ConstPixelSpacing = reader.GetPixelSpacing()

x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, -(ConstPixelDims[1]+1)*ConstPixelSpacing[1], -ConstPixelSpacing[1])
z = numpy.arange(0.0, -(ConstPixelDims[2]+1)*ConstPixelSpacing[2], -ConstPixelSpacing[2])

# Get the vtkimageData object from the reader
ImageData = reader.GetOutput()
# Get the vtkpointdata object from the vtkImageData object
PointData = ImageData.GetPointData()
# Ensure that only one array exists within the vtkpointdata object
assert (PointData.GetNumberOfArrays()==1)
# Get the vtkarray which is needed for the numpy_support.vtk_to_numpy function
ArrayData = PointData.GetArray(0)

# Convert the vtkarray to a Numpy array
ArrayDicom = numpy_support.vtk_to_numpy(ArrayData)

# Reshape the Numpy array to 3D using 'ConstPixelDims' as a 'shape'
ArrayDicom = ArrayDicom.reshape(ConstPixelDims, order='F')

ResArray = ndinter.zoom(ArrayDicom, ConstPixelSpacing, order=1)
print(ResArray[:,:,100])