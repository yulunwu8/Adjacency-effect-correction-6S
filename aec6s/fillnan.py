
# Source: https://github.com/acolite/acolite/blob/main/acolite/shared/fillnan.py

def fillnan(data):
    from scipy.ndimage import distance_transform_edt
    import numpy as np

    ## fill nans with closest value
    ind = distance_transform_edt(np.isnan(data), return_distances=False, return_indices=True)
    return(data[tuple(ind)])
