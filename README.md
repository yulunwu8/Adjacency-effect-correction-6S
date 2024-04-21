# Adjacency-effect-correction-6S
 
Based on Vermote et al. 1997

Applies to ACOLITE output only 

Edit surface reflectance 

## Installation 

1 - Create a conda environment and activate it: 

```bash
conda create --name aec6s python=3.12
conda activate aec6s
```

2 - Install dependencies: 

```bash
conda install -c conda-forge Py6S
```


temporary 

```bash
pip3 install netCDF4 numpy pandas scipy
```



3 - Install tmart: 

```bash
pip3 install aec6s
```



Input has to be ACOLITE L2R files 

It is recommended to use subscene processing in ACOLITE to reduce processing the processing time