import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d



# Define the function F_r(r)
def F_r(r):
    r_ = r/1000
    
    return 1 - 0.930 * np.exp(-0.08 * r_) - 0.070 * np.exp(-1.1 * r_)

# Distance from 1m to 2000m
r_values = np.arange(5, 1010, 5)

# Calculate the corresponding F_r values
F_r_values = F_r(r_values)

# Calculate the weight of each band
weights = np.diff(F_r_values, prepend=0)  


### Normalize by area 


# Areas of the circles with the given radii
circle_areas = np.pi * r_values ** 2

# Calculate areas of the bands
band_areas = circle_areas[1:] - circle_areas[:-1]

# Relative areas of the bands compared to the first circle
relative_band_areas = band_areas / circle_areas[0]

relative_band_areas = np.insert(relative_band_areas,0,1)


weights_nl = weights / relative_band_areas


# Create an interpolation function
interpolator = interp1d(r_values, weights_nl, kind='linear')



# Step 1: Create a 2D grid representing the 101x101 array with center at (50, 50)
size = 101  # 101x101 grid
center = size // 2  # The central point (50, 50)


# Create meshgrid for coordinates
x = np.arange(size)
y = np.arange(size)
xx, yy = np.meshgrid(x, y)

# Calculate the distance from the center for each pixel
distances = np.sqrt((xx - center)**2 + (yy - center)**2) * 10

# Clip distances 
clipped_distances = np.clip(distances, np.min(r_values), np.max(r_values))


# Apply interpolation to distances to get weights for each pixel
interpolated_weights = interpolator(clipped_distances)

# Normalize 

PSF = interpolated_weights / np.sum(interpolated_weights)



# Step 3: Visualize the result (optional)
plt.imshow(PSF, cmap='viridis', origin='lower')
plt.colorbar(label='Weights')
plt.title('PSF')
plt.show()



