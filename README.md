# PyLSCI

A Python Package for Laser Speckle Contrast Imaging.

It converts raw laser speckle data (as 2D or 3D NumPy arrays) to laser speckle contrast images (a 2D NumPy array). 

---

The code for this package was developed for my thesis on 
[Fingerprint Presentation Attack Detection using Laser Speckle Contrast Imaging](https://www.researchgate.net/publication/329391997_Fingerprint_Presentation_Attack_Detection_using_Laser_Speckle_Contrast_Imaging):

- Keilbach, P., Kolberg, J., Gomez-Barrero, M., Busch, C., & Langweg, H. (2018). Fingerprint Presentation Attack Detection using Laser Speckle Contrast Imaging. International Conference of the Biometrics Special Interest Group (BIOSIG), Darmstadt, 2018, pp. 1-6, doi: https://10.23919/BIOSIG.2018.8552931.

## Installation

```sh
pip install pylsci
```

## Dependencies

The PyLSCI packages depends on [NumPy](https://numpy.org/), 
which is is used to do all the array related calculations.

## Workflow

To work with this package, you need to have you laser speckle images available as 2D or 3D NumPy arrays:

- For spatial contrast calculation, PyLSCI expects a single, raw laser speckle image as a 2D NumPy Array.
- For temporal or spatio-temporal contrast calculation, 
PyLSCI expects a time series of multiple raw laser speckle images as a 3D NumPy Array.

Raw Laser Speckle Image (2D or 3D NumPy Array) :point_right: PyLSCI :point_right: Laser Speckle Contrast Image (2D NumPy Array)

> The process of converting the raw laser speckle images to NumPy arrays is out of scope of the `pylsci` package,
> since this process is highly dependent on a particular LSCI setup.
> See the demo notebook for an example.   

## Usage

```python
from pylsci import Lsci
# for this example, it is assumed you have a custom helper module (here it is the util.py module)
# that is responsible for converting your raw laser speckle images to the NumPy arrays expected by PyLSCI
from util import convert_speckle_to_numpy

# 1. Loading Raw Laser Speckle Data to NumPy Arrays
# 
# speckle_img represents a single laser speckle image as 2D NumPy array for spatial contrast ccalculation
speckle_img = convert_speckle_to_numpy('img/spatial.tif')
# speckle_img_sequence represents a time series of speckle images as a NumPy 3D array 
# for temporal or spatio-temporal contrast calculation,
# where the first dimension is the number of images
speckle_img_sequence = convert_speckle_to_numpy('img/temporal.png', temporal_series=True)

# 2. Create a Lsci Object
# 
# you can pass custom values for the spatial and temporal neighborhoos arguments nbh_s and nbh_t.
# Their values default to nbh_s=3 and nbh_t=25 if you omit them.
# Note that nbh_s needs to be an odd value, but there is no constraint for nbh_t
lsci = Lsci(nbh_s=5, nbh_t=40)

# 3. Calculate the Laser Speckle Contrast Images
#
# 3.1 Spatial Contrast Calculation 
# The spatial contrast calculation requires a single laser speckle image as a NumPy 2D array
# and returns a single laser speckle contrast image as a 2D NumPy array.
s_lsci = lsci.spatial_contrast(speckle_img)

# 3.2 Temporal Contrast Calculation
# The temporal and spatio-temporal contrast calculation require a 3D NumPy array (time series of laser speckle images)
# and will return a single (averaged) laser speckle contrast image as a 2D NumPy array.
t_lsci = lsci.temporal_contrast(speckle_img_sequence)
st_lsci = lsci.spatio_temporal_contrast(speckle_img_sequence)

```

## Implementation Details

Note that the iterations of the 2D or 3D arrays are not (yet) optimized. 
The `temporal_contrast()` function performs quite well, 
since NumPy allows to calculate the standard deviation and mean along the temporal axis for the whole array.
This is not the case for the `spatial_contrast()` and `spatio_temporal_contrast()` functions,
where the implementations rely on inefficient, nested loops.

Please be aware of this as calculating the contrast 
with the `spatial_contrast()` and `spatio_temporal_contrast()` functions may take a long time.


## Further Reading

To understand the theory and concepts of LSCI, the following papers are recommended:

- Boas, D. A., & Dunn, A. K. (2010). Laser speckle contrast imaging in biomedical optics. Journal of biomedical optics, 15(1), 011109. https://doi.org/10.1117/1.3285504
- Vaz, P. G., Humeau-Heurtier, A., Figueiras, E., Correia, C., & Cardoso, J. (2016). Laser Speckle Imaging to Monitor Microvascular Blood Flow: A Review. IEEE reviews in biomedical engineering, 9, 106–120. https://doi.org/10.1109/RBME.2016.2532598
- Senarathna, J., Rege, A., Li, N., & Thakor, N. V. (2013). Laser Speckle Contrast Imaging: theory, instrumentation and applications. IEEE reviews in biomedical engineering, 6, 99–110. https://doi.org/10.1109/RBME.2013.2243140
- Briers, D., Duncan, D. D., Hirst, E., Kirkpatrick, S. J., Larsson, M., Steenbergen, W., Stromberg, T., & Thompson, O. B. (2013). Laser speckle contrast imaging: theoretical and practical limitations. Journal of biomedical optics, 18(6), 066018. https://doi.org/10.1117/1.JBO.18.6.066018

