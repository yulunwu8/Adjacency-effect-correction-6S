
def run(file, anci_folder, username, password, overwrite=False, to_log = True):
    import os, sys, time
    from importlib.metadata import version
    from .read_metadata import read_metadata
    from .get_ancillary import get_ancillary
    from .AEC import AEC
    
    ### Logging  
    if to_log: 
        # Start logging in txt file
        orig_stdout = sys.stdout
        
        # log_file = out_file.replace(".csv", ".txt")
        log_file = 'log_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.txt'
        log_file = os.path.join(anci_folder, log_file)
    
    
        class Logger:
            def __init__(self, filename):
                self.console = sys.stdout
                self.file = open(filename, 'w')
                self.file.flush()
            def write(self, message):
                self.console.write(message)
                self.file.write(message)
            def flush(self):
                self.console.flush()
                self.file.flush()
    
        sys.stdout = Logger(log_file)
    
    # Paths 
    home_folder = os.path.dirname(file)
    basename = os.path.basename(file)
    basename_before_period = basename.split('.')[0]
    
    # Metadata
    print('aec6s version: ' + str(version('aec6s')))
    print('System time: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print('file: ' + str(file))
    print('anci_folder: ' + str(anci_folder))
    print('overwrite: ' + str(overwrite))
    
    ### Default: create a new file named AEC_xxx in the same folder
    
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
    print('\nMetadata: ')
    for k, v in metadata.items():
        print(str(k) + ': '  + str(v))
    
    ### Download ancillary and extract information 
    anci = get_ancillary(metadata, username, password, anci_folder)
    
    ### AEC
    AEC(metadata, anci)
    
    print('\nAE Correction complete.')
    
    if not overwrite: print('New file: ' + str(file))
    
    # Stop logging 
    if to_log: sys.stdout = orig_stdout
    