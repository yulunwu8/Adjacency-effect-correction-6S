# Adjacency-effect-correction-6S
 
This *aec6s* project implements the Vermote et al. (1997) approach to correct for the adjacency effect, utilizing the setup in Martins et al. (2018). This tool was designed specifically for ACOLITE output L2R files.

It is recommended to use subscene processing in ACOLITE to reduce the processing time of *aec6s*.



### References 

Martins, V. S., Kaleita, A., Barbosa, C. C. F., Fassoni-Andrade, A. C., Lobo, F. de L., & Novo, E. M. L. M. (2019). Remote sensing of large reservoir in the drought years: Implications on surface water change and turbidity variability of Sobradinho reservoir (Northeast Brazil). Remote Sensing Applications: Society and Environment, 13, 275–288. https://doi.org/10.1016/j.rsase.2018.11.006

Vermote, E. F., El Saleous, N., Justice, C. O., Kaufman, Y. J., Privette, J. L., Remer, L., Roger, J. C., & Tanré, D. (1997). Atmospheric correction of visible to middle‐infrared EOS‐MODIS data over land surfaces: Background, operational algorithm and validation. Journal of Geophysical Research: Atmospheres, 102(D14), 17131–17141. https://doi.org/10.1029/97JD00201



## Installation 

1 - Create a conda environment and activate it: 

```bash
conda create --name aec6s python=3.12
conda activate aec6s
```

2 - Install Py6S from conda: 

```bash
conda install -c conda-forge Py6S
```

3 - Install aec6s: 

```bash
pip3 install aec6s
```



## Quick Start

```python
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
```



