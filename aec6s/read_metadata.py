
def read_metadata(file):
    
    import netCDF4 as nc4
    import numpy as np
    from datetime import datetime
    import Py6S
    import sys
    
    # Open netcdf file 
    dset = nc4.Dataset(file, 'r+')
    
    # read Attributes 
    sensor = dset.getncattr('sensor')
    
    # date time
    isodate = dset.getncattr('isodate')
    datetime_str = isodate[0:19]
    datetime_obj = datetime.fromisoformat(datetime_str)
    
    # geometry
    sza = dset.getncattr('sza')
    vza = dset.getncattr('vza')
    vaa = dset.getncattr('vaa')
    saa = dset.getncattr('saa')
    
    # pixel size 
    pixel_size = dset.getncattr('scene_pixel_size')[0]
    
    # Create dictionary 
    metadata =  {'file': file,
                 'sensor': sensor,
                 'datetime':datetime_obj, # object
                 'time':datetime_str, # string
                 'saa':saa,
                 'sza':sza,
                 'vaa':vaa,
                 'vza':vza,
                 'pixel_size':pixel_size}
    
    # latlon 
    try:
        limit = dset.getncattr('limit')
        metadata['lat'] = np.mean(limit[[0,2]])
        metadata['lon'] = np.mean(limit[[1,3]])
        
    except:
        metadata['lat'] = np.mean(dset['lat'][:])
        metadata['lon'] = np.mean(dset['lon'][:])

    ### bands and wavelengths 
    
    if sensor == 'S2A_MSI': 
        metadata['AEC_bands_6S'] = [Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_01),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_02),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_03),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_04),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_05),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_06),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_07),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_08),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_8A),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_11),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2A_MSI_12)]
        metadata['AEC_bands_wl'] = [442.7, 492.4, 559.8, 664.6, 704.1, 740.5, 782.8, 832.8, 864.7, 1613.7, 2202.4]
        ACOLITE_bands = [443,492,560,665,704,740,783,833,865,1614,2202]
        
    elif sensor == 'S2B_MSI':
        metadata['AEC_bands_6S'] = [Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_01),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_02),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_03),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_04),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_05),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_06),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_07),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_08),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_8A),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_11),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.S2B_MSI_12)]
        metadata['AEC_bands_wl'] = [442.2, 492.1, 559.0, 664.9, 703.8, 739.1, 779.7, 832.9, 864.0, 1610.4, 2185.5]
        ACOLITE_bands = [442,492,559,665,704,739,780,833,864,1610,2186]
    
    elif sensor =='L8_OLI':
    
        metadata['AEC_bands_6S'] = [Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B1),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B2),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B3),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B4),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B5),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B6),
                                    Py6S.Wavelength(Py6S.PredefinedWavelengths.LANDSAT_OLI_B7)]
        
        # Center wavelength, source: http://gsics.atmos.umd.edu/pub/Development/20171106/5k_Ong_Landsat8_Lunar_Calibrations.pdf
        metadata['AEC_bands_wl'] = [443, 482, 561.4, 654.6, 864.7, 1608.9, 2200.7]
        ACOLITE_bands = [443, 483, 561, 655, 865, 1609, 2201]
    
    elif sensor == 'L9_OLI':
        
        # source: https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-instruments/oli-2-design/oli-2-relative-spectral-response/
        metadata['AEC_bands_6S'] = _L9_RSR()
        metadata['AEC_bands_wl'] = [442.81, 481.89, 560.95, 654.32, 864.64, 1608.15, 2200.12]
        
        # Add ACOLITE_bands!!! 
        sys.exit('Missing L9 OLI bands for ACOLITE, contact Yulun at yulunwu8@gmail.com')
        
    else:
        sys.exit('Unknown sensor.')
        
    metadata['ACOLITE_bands'] =  [f'rhos_{band}' for band in ACOLITE_bands]
        
    return metadata

def _L9_RSR():
    from Py6S import Wavelength 
    
    # B1
    bands = [Wavelength(0.425, 0.46, [0.000101538, 0.001853745, 0.003605952, 0.250039841, 0.49647373, 0.745605916, 0.994738102, 0.9887387155, 0.982739329, 0.8116886615000001, 0.640637994, 0.3245583315, 0.008478669, 0.00433083, 0.000182991]),
             
             # B2
             Wavelength(0.44, 0.54, [0.000264652, 0.0022484460000000003, 0.00423224, 0.0661663475, 0.128100455, 0.499303967, 0.870507479, 0.874936849, 0.879366219, 0.886512965, 0.893659711, 0.864751607, 0.835843503, 0.851678073, 0.867512643, 0.8921797275, 0.916846812, 0.9297226965000001, 0.942598581, 0.9448266325000001, 0.947054684, 0.9241131840000001, 0.901171684, 0.926530838, 0.951889992, 0.95243907, 0.952988148, 0.9381088915, 0.923229635, 0.4680780815, 0.012926528, 0.0072643644999999995, 0.001602201, 0.000915034, 0.000227867, 0.000228843, 0.000229819, 0.0001999565, 0.000170094, 0.000104447, 3.88e-05]),
             
             # B3
             Wavelength(0.505, 0.615, [7.81e-05, 0.000148264, 0.000218428, 0.000403884, 0.00058934, 0.0011924765, 0.001795613, 0.007561864, 0.013328115, 0.0778010835, 0.142274052, 0.501638606, 0.86100316, 0.9094860255, 0.957968891, 0.9645043015000001, 0.971039712, 0.970696598, 0.970353484, 0.9839520749999999, 0.997550666, 0.9939731654999999, 0.990395665, 0.9907722175, 0.99114877, 0.987446934, 0.983745098, 0.9915458260000001, 0.999346554, 0.994333565, 0.989320576, 0.960589826, 0.931859076, 0.6384707985, 0.345082521, 0.178756953, 0.012431385, 0.006562364, 0.000693343, 0.0004103005, 0.000127258, 0.000119937, 0.000112616, 0.000105758, 9.89e-05]),
             
             # B4
             Wavelength(0.62, 0.71, [0.000100211, 0.00031119, 0.000522169, 0.004329362, 0.008136555, 0.142064355, 0.275992155, 0.6293162704999999, 0.982640386, 0.9759064614999999, 0.969172537, 0.9830198285, 0.99686712, 0.9827772975, 0.968687475, 0.968303472, 0.967919469, 0.977742672, 0.987565875, 0.976248622, 0.964931369, 0.5351438115, 0.105356254, 0.0545120235, 0.003667793, 0.002137435, 0.000607077, 0.0004015485, 0.00019602, 0.0001495435, 0.000103067, 0.0001440925, 0.000185118, 0.0001550965, 0.000125075, 0.00011013749999999999, 9.52e-05]),
             
             # B5
             Wavelength(0.81, 0.9, [0.000105104, 0.0001355095, 0.000165915, 0.00019916, 0.000232405, 0.00029023, 0.000348055, 0.0004117955, 0.000475536, 0.0007788755, 0.001082215, 0.0024862829999999997, 0.003890351, 0.017507217, 0.031124083, 0.23786219849999998, 0.444600314, 0.7176250665, 0.990649819, 0.992818862, 0.994987905, 0.9965418875000001, 0.99809587, 0.9989148675, 0.999733865, 0.9871254265, 0.974516988, 0.6468600185, 0.319203049, 0.17056571250000002, 0.021928376, 0.011963775999999999, 0.001999176, 0.001163036, 0.000326896, 0.00020174800000000002, 7.66e-05]),
             
             # B6
             Wavelength(1.52, 1.695, [0.001586258, 0.002086596, 0.002586934, 0.0035115215, 0.004436109, 0.006189855499999999, 0.007943602, 0.0108159655, 0.013688329, 0.020402463, 0.027116597, 0.042134749, 0.057152901, 0.090146417, 0.123139933, 0.192586698, 0.262033463, 0.3794444505, 0.496855438, 0.621222079, 0.74558872, 0.819251746, 0.892914772, 0.9169532954999999, 0.940991819, 0.9453653394999999, 0.94973886, 0.9495157599999999, 0.94929266, 0.9495918750000001, 0.94989109, 0.9527430530000001, 0.955595016, 0.9574170705, 0.959239125, 0.9603245555, 0.961409986, 0.962754965, 0.964099944, 0.9672558904999999, 0.970411837, 0.9750477075, 0.979683578, 0.9839055240000001, 0.98812747, 0.9933854045, 0.998643339, 0.99186486, 0.985086381, 0.9229645725, 0.860842764, 0.7192707060000001, 0.577698648, 0.43199390150000005, 0.286289155, 0.20619690400000001, 0.126104653, 0.08936134200000001, 0.052618031, 0.0376575815, 0.022697132, 0.0165751695, 0.010453207, 0.0079079605, 0.005362714, 0.0040255555, 0.002688397, 0.002053007, 0.001417617, 0.0011114565, 0.000805296]),
             
             # B7
             Wavelength(2.04, 2.35, [0.001165524, 0.0013657934999999999, 0.001566063, 0.0018802159999999999, 0.002194369, 0.002698256, 0.003202143, 0.004003555000000001, 0.004804967, 0.006170192, 0.007535417, 0.009591365, 0.011647313, 0.015378692, 0.019110071, 0.0257818135, 0.032453556, 0.044652965, 0.056852374, 0.079261178, 0.101669982, 0.140504211, 0.17933844, 0.2431232405, 0.306908041, 0.396720886, 0.486533731, 0.5800998655, 0.673666, 0.7408077120000001, 0.807949424, 0.8466885685000001, 0.885427713, 0.9029631615, 0.92049861, 0.9280699495, 0.935641289, 0.94007957, 0.944517851, 0.9465489985, 0.948580146, 0.9505155085, 0.952450871, 0.9544967710000001, 0.956542671, 0.95959571, 0.962648749, 0.964045465, 0.965442181, 0.967006773, 0.968571365, 0.968683958, 0.968796551, 0.9703031179999999, 0.971809685, 0.9722536205, 0.972697556, 0.9750495255, 0.977401495, 0.9787347314999999, 0.980067968, 0.9799933135, 0.979918659, 0.9813792109999999, 0.982839763, 0.9791260955000001, 0.975412428, 0.9752147495000001, 0.975017071, 0.9751047495, 0.975192428, 0.9758549335, 0.976517439, 0.978619695, 0.980721951, 0.9808817805000001, 0.98104161, 0.9818051755, 0.982568741, 0.9846930505, 0.98681736, 0.9881915450000001, 0.98956573, 0.9879832865, 0.986400843, 0.983405322, 0.980409801, 0.9781909584999999, 0.975972116, 0.975639105, 0.975306094, 0.9790718855, 0.982837677, 0.9895956515, 0.996353626, 0.995330572, 0.994307518, 0.9569031895, 0.919498861, 0.8278144599999999, 0.736130059, 0.6139125825, 0.491695106, 0.38787415599999997, 0.284053206, 0.2211926205, 0.158332035, 0.12271169200000001, 0.087091349, 0.0682318435, 0.049372338, 0.0394192395, 0.029466141, 0.0237512525, 0.018036364, 0.014595295, 0.011154226, 0.0092687255, 0.007383225, 0.006104451, 0.004825677, 0.0040221935, 0.00321871, 0.002699694, 0.002180678])]
    
    return bands 


