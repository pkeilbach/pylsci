# PyLSCI

A Python Package for Laser Speckle Contrast Imaging.

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
since it is used to do all the array related calculations.

## Usage

```python
from pylsci import Lsci

# you will somehow need to convert raw speckle images to numpy arrays, eg using matplotlib
from matplotlib import pyplot as plt

# you will need speckle images as numpy 2D array (single speckle image) for spatial contrast calculation ...
speckle_img = plt.imread('img/spatial.tif')
# or a sequence of speckle images as a numpy 3D array (time series of speckle images) 
# for temporal or spatio-temporal contrast calculation
# stack_images() is some custom function that converts the image sequence to a 3D array
speckle_img_sequence = plt.imread('img/temporal.png').stack_images()

# create an Lsci object
lsci = Lsci()

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

- Boas, D. A., & Dunn, A. K. (2010). Laser speckle contrast imaging in biomedical optics. Journal of biomedical optics, 15(1), 011109. https://doi.org/10.1117/1.3285504
- Vaz, P. G., Humeau-Heurtier, A., Figueiras, E., Correia, C., & Cardoso, J. (2016). Laser Speckle Imaging to Monitor Microvascular Blood Flow: A Review. IEEE reviews in biomedical engineering, 9, 106–120. https://doi.org/10.1109/RBME.2016.2532598
- Senarathna, J., Rege, A., Li, N., & Thakor, N. V. (2013). Laser Speckle Contrast Imaging: theory, instrumentation and applications. IEEE reviews in biomedical engineering, 6, 99–110. https://doi.org/10.1109/RBME.2013.2243140
- Briers, D., Duncan, D. D., Hirst, E., Kirkpatrick, S. J., Larsson, M., Steenbergen, W., Stromberg, T., & Thompson, O. B. (2013). Laser speckle contrast imaging: theoretical and practical limitations. Journal of biomedical optics, 18(6), 066018. https://doi.org/10.1117/1.JBO.18.6.066018

