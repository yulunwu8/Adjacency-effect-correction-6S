# AEC for one band 

def AEC(metadata, anci):
    from .get_parameters import get_parameters
    from .fillnan import fillnan
    import netCDF4 as nc4
    import numpy as np
    import scipy
    import time
    
    # Open netcdf file 
    dset = nc4.Dataset(metadata['file'], 'r+')
    
    # For each band 
    for i in range(len(metadata['ACOLITE_bands'])):

        ACOLITE_band = metadata['ACOLITE_bands'][i] 
        wl = metadata['AEC_bands_wl'][i]
        AEC_band_6S = metadata['AEC_bands_6S'][i]
        
        print('\n============= AEC: {} ==================='.format(ACOLITE_band))

        # Run 6S and others to get correction parameters 
        AEC_parameters = get_parameters(metadata, anci, AEC_band_6S)
        
        PSF = AEC_parameters['PSF']
        
        dif2dir = AEC_parameters['dif2dir']
        print('Diffuse to direct ratio: '+ str(dif2dir))
        
        # Load band data
        image = dset[ACOLITE_band][:].data
        is_nan = np.isnan(image)
        image = fillnan(image)
        
        # Convolution 
        start_time = time.time()
        print("\nConvolution started ")
        image_conv = scipy.signal.convolve2d(image, PSF, mode='same', boundary='fill', fillvalue=image.mean())
        print("Convolution completed: %s seconds " % (time.time() - start_time))
        
        output = image + dif2dir * (image - image_conv)
        
        # add nan back
        output[is_nan] = np.nan
        
        # Modify L2R NC file 
        dset[ACOLITE_band][:] = output
        
    # Close file 
    dset.close()
        