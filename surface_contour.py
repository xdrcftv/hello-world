import vtk
import numpy as np
from vtk.util import numpy_support
import scipy.ndimage.interpolation as ndinter

from vtk.util.misc import  vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Create the renderer, the render window, and the interactor.
# The renderer draws into the render window, the interactor enables mouse
# and keyboard-based interaction with the scene
aRenderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(aRenderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

"""
The following reader is used to read a series of 2D 
"""
v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(VTK_DATA_ROOT+"/Data/headsq/quarter")
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)

"""
An isosurface, or contour value of 500 is known to correspond to the skin of the patient. Once generated,
a vtkPolyDataNormals filter is used to create normals for smooth surface shading during rendering.
The triangle stripper is used to create triangle strips from the isosurface these render much faster on many
systems
"""
skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(v16.GetOutputPort())
skinExtractor.SetValue(0, 500) # https://en.wikipedia.org/wiki/Hounsfield_scale

skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)

skinStripper = vtk.vtkStripper()
skinStripper.SetInputConnection(skinNormals.GetOutputPort())

skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinStripper.GetOutputPort())
skinMapper.ScalarVisibilityOff()

skin = vtk.vtkActor()
skin.SetMapper(skinMapper)
skin.GetProperty().SetDiffuseColor(1, .49, .25)
skin.GetProperty().SetSpecular(.3)
skin.GetProperty().SetSpecularPower(20)

boneExtractor = vtk.vtkContourFilter()
boneExtractor.SetInputConnection(v16.GetOutputPort())
boneExtractor.SetValue(0, 1150)

boneNormals = vtk.vtkPolyDataNormals()
boneNormals.SetInputConnection(boneExtractor.GetOutputPort())
boneNormals.SetFeatureAngle(60.0)
boneStripper = vtk.vtkStripper()
boneStripper.SetInputConnection(boneNormals.GetOutputPort())
boneMapper = vtk.vtkPolyDataMapper()
boneMapper.SetInputConnection(boneStripper.GetOutputPort())
boneMapper.ScalarVisibilityOff()
bone = vtk.vtkActor()
bone.SetMapper(boneMapper)
bone.GetProperty().SetDiffuseColor(1, 1, .9412)

# An outline provides context around the data
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.ComputeViewPlaneNormal()

aRenderer.AddActor(outline)
aRenderer.AddActor(skin)
aRenderer.AddActor(bone)
aRenderer.SetActiveCamera(aCamera)
aRenderer.ResetCamera()
aCamera.Dolly(1.5)

aRenderer.SetBackground(1, 1, 1)
renWin.SetSize(640, 480)

aRenderer.ResetCameraClippingRange()

iren.Initialize()
renWin.Render()
iren.Start

