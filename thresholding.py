import vtk
from vtk.util import numpy_support
from matplotlib import pyplot
import numpy as np
import Heatmap

PathDicom = 'C:/Users/HH211/Desktop/BNCT_TEMP_20190812/CT_Image'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()

# Load dimensions using 'GetDataExtent'
_extent = reader.GetDataExtent()
ConstPixelDims = [_extent[1] - _extent[0] + 1, _extent[3] - _extent[2] + 1, _extent[5] - _extent[4] + 1]

# Load spacing values
ConstPixelSpacing = reader.GetPixelSpacing()

x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, -(ConstPixelDims[1]+1)*ConstPixelSpacing[1], -ConstPixelSpacing[1])
z = np.arange(0.0, -(ConstPixelDims[2]+1)*ConstPixelSpacing[2], -ConstPixelSpacing[2])


threshold = vtk.vtkImageThreshold()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByLower(400) # remove all soft tissue
threshold.ReplaceInOn() # Determines whether to replace the pixel in range with inValue
threshold.SetInValue(0) # Replace the in range pixels with this value
threshold.ReplaceOutOn() # Determines whether to replace the pixel out of range with OutValue
threshold.SetOutValue(1) # Replace the in range pixels with this value
threshold.Update()


# Plot thresholded image
ArrayThreshold = Heatmap.vtkImagetoNumpy(threshold.GetOutput(), ConstPixelDims)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, np.rot90(ArrayThreshold[:,:,30]))
print(ArrayThreshold[:,:,30])
pyplot.show()

