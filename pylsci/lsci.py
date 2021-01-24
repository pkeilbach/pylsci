import numpy as np


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

    @staticmethod
    def calc_spatio_temporal_contrast(cuboid: np.ndarray) -> float:
        std = np.std(cuboid)
        mean = np.mean(cuboid)
        return Lsci.contrast(std, mean)

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

    def spatial_contrast(self, speckle_img: np.ndarray) -> np.ndarray:

        # kernel size to iterate the image is the spatial neighborhood
        k = self.nbh_spat

        # create the array for the contrast values, needs to be same size as speckle image
        s_lsci = np.zeros(speckle_img.shape)

        # get image dimensions
        rows, cols = speckle_img.shape

        # spatial border margin
        m_s = int(k / 2)

        # iterate the image row by row but leave space for margins
        # for each pixel ...
        for u in range(m_s, rows - m_s):
            for v in range(m_s, cols - m_s):
                a = u - m_s
                b = u + m_s + 1
                c = v - m_s
                d = v + m_s + 1

                patch = speckle_img[a:b, c:d]
                s_lsci[u, v] = self.calc_spatial_contrast(patch)

        return s_lsci

    def temporal_contrast(self, img_stack: np.ndarray) -> np.ndarray:

        # get dimensions
        stack_size, width, height = img_stack.shape

        # determine number of lsci images that will be calculated from the image stack over the temporal neighborhood
        n = int(stack_size / self.nbh_temp)

        # create array for lsci images that will be caluclated, size n is depending on the temporal neighborhood
        t_lsci = np.zeros([n, width, height])

        # temporal margin
        # in case nbh does not match s, equally omit first and last images in layer
        # e.g. 1000 / 15 = 66 rem 10 --> shift start index 10/2 = 5 images
        # for 1000 / 25 = 40 rem 0 --> start will be 0 as usual
        m_t = int((stack_size % self.nbh_temp) / 2)

        if self.nbh_temp == 3:
            m_t = 1

        # set start index
        start = m_t
        # set end index of the first lsci images that will be calculated to the nbh over which it should be calculated
        end = stack_size - m_t
        # the step size is the temporal neighborhood
        step = self.nbh_temp

        # from the cuboid of s=1000 laser speckle images, lsci images will be calculated in layers of nbh
        # iterate all s=1000 images, depending on nbh, calculate multiple lsci images
        for i in range(start, end, step):
            # start with start index, end at the specified neighborhood
            # layer = img_stack[start:end, :, :]
            j = i + step
            layer = img_stack[i:j, :, :]

            # store the calculated values at the correct index in the lsci image array
            x = int(i / step)
            t_lsci[x, :, :] = self.calc_temporal_contrast(layer)

        # average the lsci image stack to return a single averaged t_lsci image
        return np.mean(t_lsci, axis=0)

    def spatio_temporal_contrast(self, img_stack: np.ndarray, cubic: bool = False) -> np.ndarray:
        # cubic = isotropic vs anisotropic (see Vaz' paper)

        # get dimensions
        stack_size, width, height = img_stack.shape

        # kernel size to iterate the image is the spatial neighborhood
        k_s = self.nbh_spat
        k_t = self.nbh_temp

        # check if we want to iterate the temporal domain with the same nbh as the spatial domain
        if cubic:
            k_t = k_s

        # determine number of lsci images that will be calculated from the image stack over the temporal neighborhood
        n = int(stack_size / k_t)

        # create array for lsci images that will be caluclated, size n is depending on the temporal neighborhood
        st_lsci = np.zeros([n, width, height])

        # border margins
        m_s = int(k_s / 2)
        m_t = int((stack_size % k_t) / 2)

        # special case for margin handling if temporal nbh is 3
        if cubic and k_t == 3:
            m_t += 1

        start = m_t
        end = stack_size - m_t

        for i in range(start, end, k_t):
            for w in range(m_s, width - m_s):
                for h in range(m_s, height - m_s):
                    a = i
                    b = i + k_t
                    c = w - m_s
                    d = w + m_s + 1
                    e = h - m_s
                    f = h + m_s + 1

                    x = int(i / k_t)

                    cuboid = img_stack[a:b, c:d, e:f]
                    st_lsci[x, w, h] = self.calc_spatio_temporal_contrast(cuboid)

        return np.mean(st_lsci, axis=0)
