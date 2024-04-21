







def run(file, anci_folder, username, password, overwrite=False):
    
    import os
    from .read_metadata import read_metadata
    from .get_ancillary import get_ancillary
    from .AEC import AEC
    
    
    ### Set up printing 
    
    # Paths 
    home_folder = os.path.dirname(file)
    basename = os.path.basename(file)
    basename_before_period = basename.split('.')[0]
    
    
    ### Default: create a new file named AEC_xxx
    
    if not overwrite: 
        basename_new = 'AEC_' + basename
        file_new = os.path.join(home_folder,basename_new)
        
        from shutil import copy
        copy(file, file_new)
        
        file = file_new
        
    
    ### Ancillary 
    
    # anci_folder: if not exist -> create it 
    if not os.path.exists(anci_folder):
        os.makedirs(anci_folder)
    
    
    ### Read imagery metadata
    
    metadata = read_metadata(file)
    
    # Print metadata 
    print('Metadata: ')
    for k, v in metadata.items():
        print(str(k) + ': '  + str(v))
    
    
    ### Download ancillary and extract information 
    anci = get_ancillary(metadata, username, password, anci_folder)
    
    
    ### AEC, one band at a time 
    
    for i in range(len(metadata['ACOLITE_bands'])):
        
        # test
        # i = 8
        
        ACOLITE_band = metadata['ACOLITE_bands'][i] 
        wl = metadata['AEC_bands_wl'][i]
        AEC_band_6S = metadata['AEC_bands_6S'][i]
        
        
        print('\n============= AEC: {} ==================='.format(ACOLITE_band))
            
        AEC(metadata, anci, ACOLITE_band, wl, AEC_band_6S)
        
    
    
    
    
    
    
    

































