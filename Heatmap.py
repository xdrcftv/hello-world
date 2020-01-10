"""
작성일 2019/11/19
"""

import vtk
from vtk.util import numpy_support
import os
import numpy as np

def vtkImagetoNumpy(image, pixelDims):
    pointData = image.GetPointData()
    arrayData = pointData.GetArray(0)
    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
    ArrayDicom = ArrayDicom.reshape(pixelDims, order='F')

    return ArrayDicom

"""
def plotHeatmap(array, name="plot"):
    data = Data([
        Heatmap(
            z=array,
            scl='Greys'
        )
    ])
    layout = Layout(
        autosize=False,
        title=name
    )
    fig = Figure(data=data, layout=layout)

    return plotly.plotly.iplot(fig, filename=name)

from IPython.display import Image


def buffer(param):
    pass


def vtk_show(renderer, width=400, height=300):

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()
    
    windowToImageFilter = vtk.vtkWindowToImageFilter
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Updata()
    
    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = str(buffer(writer.GetResult()))
    
    return Image(data)
   
"""