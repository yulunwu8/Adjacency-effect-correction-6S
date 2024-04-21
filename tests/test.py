

# %matplotlib qt


# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import aec6s

# S2
file = '/Users/yw/Local_storage/S2A_MSI_2015_09_12_10_17_24_T32TPR_L2R.nc'

anci_folder = '/Users/yw/Local_storage/anci' 

username = 'abc'
password = '123'

aec6s.run(file, anci_folder, username, password, overwrite=False)


