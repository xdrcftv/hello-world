import numpy as np
import glob
import os


path = 'C:/Users/user/Desktop/N2'
asc_file_list = glob.glob(os.path.join(path, "*.asc"))

print(asc_file_list[0])
f = open(asc_file_list[0], 'r')

lines = f.readlines()
CDBS_data = []
for i in range(1024):
    count = lines[i+23].split(",")
    count = list(map(int, count))
    del count[0]
    CDBS_data.append(count)

CDBS_data = np.array(CDBS_data)
print(CDBS_data)
