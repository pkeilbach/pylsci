import numpy as np

# TODO
#   - check out if we can vectorize the image iteration:
#       https://realpython.com/numpy-array-programming/#image-feature-extraction
#       https://www.pyimagesearch.com/2017/08/28/fast-optimized-for-pixel-loops-with-opencv-and-python/


class Lsci(object):

    @staticmethod
    def get_spatial_contrast_value(speckle_img: np.ndarray, k: int, m: int, u: int, v: int) -> np.ndarray:
        # create kernel
        kernel = np.zeros((k, k))
        # fill kernel with the pixel values of the speckle image and consider margin
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                kernel[m + i, m + j] = speckle_img[u + i, v + j]

        # TODO if mean is zero handling
        # apply contrast formula and return
        return np.std(kernel) / np.mean(kernel)

    def __init__(self, nbh_spat: int = 3, nbh_temp: int = 25):
        self.nbh_spat = nbh_spat
        self.nbh_temp = nbh_temp

    @property
    def nbh_spat(self):
        return self._nbh_spat

    @nbh_spat.setter
    def nbh_spat(self, value: int):
        self._nbh_spat = value

    @property
    def nbh_temp(self):
        return self._nbh_temp

    @nbh_temp.setter
    def nbh_temp(self, value: int):
        self._nbh_temp = value

    def get_spatial_contrast_img(self, speckle_img: np.ndarray) -> np.ndarray:

        # kernel size to iterate the image is the spatial neighborhood
        k = self.nbh_spat

        # create the array for the contrast values, needs to be same size as speckle image
        contrast_img = np.zeros(speckle_img.shape)

        # get image dimensions
        r, c = speckle_img.shape

        # border margins
        m = int(k / 2)

        # iterate the image row by row but leave space for margins
        # for each pixel ...
        for u in range(m, r - m):
            for v in range(m, c - m):
                # ... calculate the speckle contrast
                contrast_img[u, v] = self.get_spatial_contrast_value(speckle_img, k, m, u, v)

                # TODO this seems a better approach ...
                # patch = speckle_img[u - m:u + m + 1, v - m:v + m + 1]

        return contrast_img
