


# get AEC parameters for each band 

def get_parameters(metadata, anci, AEC_band_6S):
    
    import numpy as np
    from scipy.interpolate import interp1d
    
    
    # 6S calculate: upward diffuse transmittances and dif2dir ratio 
    info_6S = run_6S(metadata, anci, AEC_band_6S)
   
    # Upward transmittances 
    t_Rayleigh = info_6S['t_Rayleigh']
    t_Aerosol = info_6S['t_Aerosol']
    
    # Diffuse to direct ratio 
    dif2dir = info_6S['dif2dir']
    
    
    # construct 1km by 1km PSF
    
    # hard code the size of PSF for now 
    PSF_length = 1000 # in unit of meter
    
    # Distance from 5m to 1010m
    pixel_size = metadata['pixel_size']
    r_values = np.arange(pixel_size/2, PSF_length, pixel_size/2)
    
    # Calculate the corresponding F_r values
    F_r_values = F_r(r_values, t_Rayleigh, t_Aerosol)

    # Calculate the weight of each band
    weights = np.diff(F_r_values, prepend=0)  


    ### Normalize by area 
    circle_areas = np.pi * r_values ** 2
    band_areas = circle_areas[1:] - circle_areas[:-1]

    # Relative areas of the bands compared to the first circle
    relative_band_areas = band_areas / circle_areas[0]
    relative_band_areas = np.insert(relative_band_areas,0,1)

    # normalized to area 
    weights_nl = weights / relative_band_areas

    # Create an interpolation function
    interpolator = interp1d(r_values, weights_nl, kind='linear')

    # PSF: number of pixels on each size 
    size = round_up_to_odd(PSF_length/pixel_size)
    center = size // 2  # The central point (50, 50)


    # Create meshgrid for coordinates
    x = np.arange(size)
    y = np.arange(size)
    xx, yy = np.meshgrid(x, y)

    # Calculate the distance from the center for each pixel
    distances = np.sqrt((xx - center)**2 + (yy - center)**2) * pixel_size
    clipped_distances = np.clip(distances, np.min(r_values), np.max(r_values)) # make sure no extrapolation 


    # Apply interpolation to distances to get weights for each pixel
    interpolated_weights = interpolator(clipped_distances)

    # Normalize to 1
    PSF = interpolated_weights / np.sum(interpolated_weights)
    
    AEC_parameters = {'PSF':PSF,
                      'dif2dir':dif2dir}

    return AEC_parameters

    
    
# Define the function F_r(r)
def F_r(radius, t_Rayleigh, t_Aerosol):
    import numpy as np
    r = radius / 1000
    
    # Calculate the Rayleigh and Aerosol contributions
    F_Rayleigh = 1 - 0.930 * np.exp(-0.08 * r) - 0.070 * np.exp(-1.1 * r)
    F_Aerosol = 1 - 0.448 * np.exp(-0.27 * r) - 0.552 * np.exp(-2.83 * r)
    
    # Calculate the combined weight 
    F_r = (t_Rayleigh * F_Rayleigh + t_Aerosol * F_Aerosol) / (t_Rayleigh + t_Aerosol)
    
    return F_r


def round_up_to_odd(num):
    import math
    # Round the number up to the nearest integer
    rounded = math.ceil(num)
    
    # If the rounded integer is even, add one to make it odd
    if rounded % 2 == 0:
        return rounded + 1
    # If the rounded integer is odd, return it as is
    else:
        return rounded


def run_6S(metadata, anci, AEC_band_6S):
    
    import Py6S
    
    s = Py6S.SixS()
    
    # geometry
    s.geometry = Py6S.Geometry.User()
    s.geometry.solar_z = metadata['sza']
    s.geometry.solar_a = metadata['saa']
    s.geometry.view_z = metadata['vza']
    s.geometry.view_a = metadata['vaa']
    
    s.altitudes.set_sensor_satellite_level()
    
    # molecules 
    s.atmos_profile = Py6S.AtmosProfile.UserWaterAndOzone(anci['water_vapour']/10, anci['ozone']/1000)
    
    # aerosol 
    r_mar = anci['r_maritime']
    r_con = 1 - r_mar
    s.aero_profile = Py6S.AeroProfile.User(soot = 0.01*r_con, water = 0.05*r_mar + 0.29*r_con, 
                                           oceanic = 0.95*r_mar, dust = 0.7*r_con)
    s.aot550 = anci['AOT_MERRA2']
    
    # band 
    s.wavelength = AEC_band_6S
    
    # run
    s.run()

    ### results 
    # print(s.outputs.fulltext)

    L_env_target = s.outputs.values['background_radiance']
    L_dir_target = s.outputs.values['pixel_radiance']
    dif2dir = L_env_target/L_dir_target
    
    t_Rayleigh = s.outputs.transmittance_rayleigh_scattering.upward
    t_Aerosol  = s.outputs.transmittance_aerosol_scattering.upward
    
    info_6S = {'dif2dir':dif2dir,
               't_Rayleigh':t_Rayleigh,
               't_Aerosol':t_Aerosol}
    
    return info_6S
    

