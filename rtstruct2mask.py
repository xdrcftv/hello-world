import os
import xml.etree.ElementTree as EleTree
import numpy as np
import pydicom as dcm

file_directory = 'C:/INFINITT/BNCT_TEMP/'

whole_files = os.listdir(file_directory)
list(whole_files)
xml_file = os.path.join(file_directory, whole_files[0])
xml_doc = EleTree.parse(xml_file)

root = xml_doc.getroot()
ROI = root.find('ROI')

tumor_ROI = []
for child in ROI:
    ITEM = ROI.find(child.tag)
    ROI_type = ITEM.findtext('ROIType')
    if ROI_type == 'Tumor':
        tumor_ROI.append(int(ITEM.findtext('ROINo')))


struct_dir = root.findtext('RTStructure')
RT_struct = dcm.dcmread(struct_dir)

ROI_contour = RT_struct.ROIContourSequence
print(ROI_contour[27])
first_slide = ROI_contour[27].ContourSequence[1].ContourData
pointNo = int(len(first_slide)/3)
pixelCoords = np.array(ROI_contour[27].ContourSequence[1].ContourData).reshape((pointNo, 3))
print(pixelCoords)

contour_array = np.zeros(512, 512).astype(bool)
cols = pixelCoords[:, 0]
rows = pixelCoords[:, 1]
contour_array[cols, rows] = True

