import numpy as np
from util import time_test

# TODO
#   - check out if we can vectorize the image iteration:
#       https://realpython.com/numpy-array-programming/#image-feature-extraction
#       https://www.pyimagesearch.com/2017/08/28/fast-optimized-for-pixel-loops-with-opencv-and-python/
#       https://medium.com/analytics-vidhya/implementing-convolution-without-for-loops-in-numpy-ce111322a7cd
#       https://medium.com/analytics-vidhya/2d-convolution-using-python-numpy-43442ff5f381
#   - spatio-temporal function


class Lsci(object):

    @staticmethod
    def contrast(std, mean):
        return std / mean

    @staticmethod
    def calc_temporal_contrast(layer: np.ndarray) -> np.ndarray:

        # apply contrast formula in layer
        # axis = 0 specifies the temporal domain
        # numpy automatically calculates std and average for all pixels in the image
        std = np.std(layer, axis=0)
        mean = np.mean(layer, axis=0)

        # if mean is zero, the contrast formula will throw an arithmetic error (division by zero)
        # hence, use small value instead
        mean[mean == 0] = 1e-25

        # apply contrast formula
        contrast = Lsci.contrast(std, mean)

        # in theory, lsci is not greater than 1.
        # In practice, tests show that this may happen due to noise or similar
        # hence, set contrast to 1 in case greater values occur.
        contrast[contrast > 1] = 1

        return contrast

    @staticmethod
    def calc_spatial_contrast(patch: np.ndarray) -> float:
        std = np.std(patch)
        mean = np.mean(patch)
        return Lsci.contrast(std, mean)

        # if safe:
        #     # dividing by zero would cause an arithmetic error,
        #     # so in case mean is 0, we divide by a really small number
        #     if np.mean(patch) == 0:
        #         mean = 1e-25
        #
        #     # apply contrast formula
        #     contrast = Lsci.contrast(std, mean)
        #
        #     if contrast > 1:
        #         contrast = 1
        #
        #     return contrast
        # else:
        #     return Lsci.contrast(std, mean)

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

    @time_test
    def spatial_contrast(self, speckle_img: np.ndarray) -> np.ndarray:

        # kernel size to iterate the image is the spatial neighborhood
        k = self.nbh_spat

        # create the array for the contrast values, needs to be same size as speckle image
        s_lsci = np.zeros(speckle_img.shape)

        # get image dimensions
        rows, cols = speckle_img.shape

        # border margins
        m = int(k / 2)

        # iterate the image row by row but leave space for margins
        # for each pixel ...
        for u in range(m, rows - m):
            for v in range(m, cols - m):
                a = u - m
                b = u + m + 1
                c = v - m
                d = v + m + 1

                s_lsci[u, v] = self.calc_spatial_contrast(patch=speckle_img[a:b, c:d])

        return s_lsci

    def temporal_contrast(self, img_stack: np.ndarray) -> np.ndarray:
        # get dimensions
        s, w, h = img_stack.shape

        # determine number of lsci images
        n = int(s / self.nbh_temp)

        # in case nbh does not match s, equally omit first and last images in layer
        # e.g. 1000 / 15 = 66 rem 10 --> shift start index 10/2 = 5 images
        # for 1000 / 25 = 40 rem 0 --> start will be 0 as usual
        shift = int((s % self.nbh_temp) / 2)

        # set start index
        start = shift
        # set end index of the first lsci images that will be calculated to the nbh over which it should be calculated
        end = self.nbh_temp

        # create array for lsci images that will be caluclated, size n is depending on the temporal neighborhood
        t_lsci = np.zeros([n, w, h])

        # from the cuboid of s=1000 laser speckle images, lsci images will be calculated in layers of nbh
        # iterate all s=1000 images, depending on nbh, calculate multiple lsci images
        for i in range(0, n):
            # start with start index, end at the specified neighborhood
            layer = img_stack[start:end, :, :]

            # store the calculated values at the ith index in the lsci image array
            t_lsci[i, :, :] = self.calc_temporal_contrast(layer)

            # set start and end index for next layer
            start = end
            end = start + self.nbh_temp

        # average the lsci image stack to return a single averaged t_lsci image
        return np.mean(t_lsci, axis=0)

    # TODO
    def spatio_temporal_contrast(self, img_stack: np.ndarray) -> np.ndarray:
        pass

    # @staticmethod
    # def get_spatial_contrast_value(speckle_img: np.ndarray, k: int, m: int, u: int, v: int) -> float:
    #     # create kernel
    #     kernel = np.zeros((k, k))
    #     # fill kernel with the pixel values of the speckle image and consider margin
    #     for i in range(-m, m + 1):
    #         for j in range(-m, m + 1):
    #             kernel[m + i, m + j] = speckle_img[u + i, v + j]
    #
    #     return np.std(kernel) / np.mean(kernel)
    #     # return Lsci.calculate_speckle_contrast(kernel)
    #     # return contrast
