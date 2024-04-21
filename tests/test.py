

# %matplotlib qt


# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import aec6s

# ACOLITE L2R file
file = '/Users/yw/Local_storage/S2A_MSI_2015_09_12_10_17_24_T32TPR_L2R.nc'

# Folder for ancillary data and logging files
anci_folder = '/Users/yw/Local_storage/anci' 

# NASA EarthData Credentials, OB.DAAC Data Access needs to be approved
username = 'abc'
password = '123'

# Run AE correction
aec6s.run(file, anci_folder, username, password, overwrite=False)


