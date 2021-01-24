# PyLSCI

Python Package for Laser Speckle Contrast Imaging

---

The code for this package was developed for my thesis on 
[Fingerprint Presentation Attack Detection using Laser Speckle Contrast Imaging](https://www.researchgate.net/publication/329391997_Fingerprint_Presentation_Attack_Detection_using_Laser_Speckle_Contrast_Imaging).


## Installation

```sh
pip install pylsci
```

## Dependencies

The PyLSCI packages depends on [NumPy](https://numpy.org/), 
since it is used to do all the array related calculations.

## Usage

```python
from pylsci import Lsci

# create an Lsci object
lsci = Lsci()

# you need an image as a 2D numpy array or a series of images as a 3D numpy array
# speckle_img  # this should be a 2D numpy array
# speckle_img_sequence  # this should be a 3D numpy array

# the spatial contrast requires a single speckle image as a numpy 2D array
s_lsci = lsci.spatial_contrast(speckle_img)

# the temporal and spatio-temporal contrast requires a 3D array (time series of speckle images)
t_lsci = lsci.temporal_contrast(speckle_img_sequence)
st_lsci = lsci.spatio_temporal_contrast(speckle_img_sequence)
```

## Implementation Details

Note that the iterations of the 2D or 3D arrays are not (yet) optimized. 
The `temporal_contrast()` function performs quite well, 
since numpy allows to calculate the standard deviation and mean along the temporal axis for the whole array.
This is not the case for the `spatial_contrast()` and `spatio_temporal_contrast()` functions,
where the implementations rely on inefficient, nested loops.

Please be aware of this as calculating the contrast 
with the `spatial_contrast()` and `spatio_temporal_contrast()` functions may take a long time.


## Further Reading

To understand the theory and concepts of LSCI, the following papers are recommended:

- Paper 1
- Paper 2
- Paper 3
