


# AEC for one band 

def AEC(metadata, anci, ACOLITE_band, wl, AEC_band_6S):
    
    
    from .get_parameters import get_parameters
    from .fillnan import fillnan
    
    import netCDF4 as nc4
    import numpy as np
    import scipy
    import time
    
    ### Run 6S and others to get correction parameters 
    
    
    AEC_parameters = get_parameters(metadata, anci, AEC_band_6S)
    
    PSF = AEC_parameters['PSF']
    
    dif2dir = AEC_parameters['dif2dir']
    
    
    # Open netcdf file 
    dset = nc4.Dataset(metadata['file'], 'r+')
    
    
    image = dset[ACOLITE_band][:].data
    
    
    is_nan = np.isnan(image)
    
    image = fillnan(image)
    
    
    # Convolution 
    start_time = time.time()
    print("\nConvolution started ")
    image_conv = scipy.signal.convolve2d(image, PSF, mode='same', boundary='fill', fillvalue=image.mean())
    print("Convolution completed: %s seconds " % (time.time() - start_time))
    
    
    
    output = image + dif2dir * (image - image_conv)
    
    
    
    
    
    
    
    
    pass


