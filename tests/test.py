

# %matplotlib qt


# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)


import aec6s



aec6s.run()




