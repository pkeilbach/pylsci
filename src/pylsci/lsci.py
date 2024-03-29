"""module which contains the Lsci class
"""

import numpy as np


class Lsci:

    """
    This class contains functionality to calculate laser speckle contrast
    in spatial, temporal, or spatio-temporal domain.

    Args:
        nbh_s (int, optional): spatial neighborhood. Defaults to NBH_S.
        nbh_t (int, optional): temporal neighborhood. Defaults to NBH_T.

    """

    # default values for spatial and temporal neighborhood
    NBH_S = 3
    NBH_T = 25

    @staticmethod
    def contrast(std, mean):
        """
        calculates the laser speckle contrast.

        Args:
            std (_type_): standard deviation.
            mean (_type_): mean.

        Returns:
            _type_: laser speckle contrast.
        """
        return std / mean

    @staticmethod
    def calc_temporal_contrast(layer: np.ndarray) -> np.ndarray:
        """
        calculates the speckle contrast in the temporal domain.

        Args:
            layer (np.ndarray): a 3D numpy array with laser speckle data.

        Returns:
            np.ndarray: a 2D numpy array of the calculated laser speckle contrast.
        """

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
    def calc_array_contrast(arr: np.ndarray) -> float:
        """
        calc_array_contrast calculates the contrast for `arr`.

        Args:
            arr (np.ndarray): a 2D numpy array.

        Returns:
            float: contrast value for `arr`.
        """
        std = np.std(arr)
        mean = np.mean(arr)
        return Lsci.contrast(std, mean)

    def __init__(self, nbh_s: int = NBH_S, nbh_t: int = NBH_T):
        self.nbh_s = nbh_s
        self.nbh_t = nbh_t

    @property
    def nbh_s(self) -> int:
        """
        spatial neighborhood for contrast calculation, must be an odd number.

        Returns:
            int: value for spatial neighborhood.
        """
        return self._nbh_s

    @nbh_s.setter
    def nbh_s(self, value: int):
        if value % 2:
            self._nbh_s = value
        else:
            self._nbh_s = Lsci.NBH_S
            print(
                f"""
                invalid value for nbh_s: use odd number as spatial neighborhood.
                Using default value of {Lsci.NBH_S}.
                """
            )

    @property
    def nbh_t(self) -> int:
        """
        temporal neighborhood for contrast calculation.

        Returns:
            int: value for temporal neighborhood.
        """
        return self._nbh_t

    @nbh_t.setter
    def nbh_t(self, value: int):
        self._nbh_t = value

    def spatial_contrast(self, speckle_img: np.ndarray) -> np.ndarray:
        """
        spatial contrast calculation.

        Args:
            speckle_img (np.ndarray): raw laser speckle as a 2D np.ndarray.

        Returns:
            np.ndarray: the calculated speckle contrast image as 2D np.ndarray.
        """

        # kernel size to iterate the image is the spatial neighborhood
        k_s = self.nbh_s

        # create the array for the contrast values, needs to be same size as speckle image
        s_lsci = np.zeros(speckle_img.shape)

        # get image dimensions
        rows, cols = speckle_img.shape

        # spatial border margin
        m_s = int(k_s / 2)

        # iterate the image row by row but leave space for margins
        # for each pixel ...
        for u in range(m_s, rows - m_s):
            for v in range(m_s, cols - m_s):
                a = u - m_s
                b = u + m_s + 1
                c = v - m_s
                d = v + m_s + 1

                patch = speckle_img[a:b, c:d]
                s_lsci[u, v] = self.calc_array_contrast(patch)

        return s_lsci

    def temporal_contrast(self, img_stack: np.ndarray) -> np.ndarray:
        """
        temporal contrast calculation.

        Args:
            img_stack (np.ndarray): a time series of raw laser speckle data as 3D np.ndarray.

        Returns:
            np.ndarray: the calculated speckle contrast image as 2D np.ndarray.
        """

        # get dimensions
        stack_size, width, height = img_stack.shape

        # get temporal neighborhood
        k_t = self.nbh_t

        # determine number of lsci images that will be calculated
        # from the image stack over the temporal neighborhood
        n = int(stack_size / k_t)

        # create array for lsci images that will be caluclated,
        # size n is depending on the temporal neighborhood
        t_lsci = np.zeros([n, width, height])

        # temporal margin
        # in case nbh does not match s, equally omit first and last images in layer
        # e.g. 1000 / 15 = 66 rem 10 --> shift start index 10/2 = 5 images
        # for 1000 / 25 = 40 rem 0 --> start will be 0 as usual
        m_t = int((stack_size % k_t) / 2)

        # special margin case if k_t is 3:
        # 999 -> rem 1: int((1 % 3) / 2) = 0 -> no margin
        # but no margin would lead to wrong indexing in t_lsci array (one too long)
        # so to avoid that, we set the margin to 1
        if k_t == 3:
            m_t = 1

        # set start index
        start = m_t
        # set end index of the first lsci images that will be calculated
        # to the nbh over which it should be calculated
        end = stack_size - m_t
        # the step size is the temporal neighborhood
        step = k_t

        # from the cuboid of s=1000 laser speckle images,
        # lsci images will be calculated in layers of nbh
        # iterate all s=1000 images, depending on nbh,
        # calculate multiple lsci images
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

    def spatio_temporal_contrast(
        self, img_stack: np.ndarray, cubic: bool = False
    ) -> np.ndarray:
        """
        spatio-temporal contrast calculation.

        Args:
            img_stack (np.ndarray): a time series of raw laser speckle data as 3D np.ndarray.
            cubic (bool, optional): isotropic vs. anisotropic,
                see Vaz et al.: https://doi.org/10.1109/RBME.2016.2532598.
                Defaults to False.

        Returns:
            np.ndarray: the calculated speckle contrast image as 2D np.ndarray.
        """
        # cubic = isotropic vs anisotropic (see Vaz' paper)

        # get dimensions
        stack_size, width, height = img_stack.shape

        # kernel size to iterate the image is the spatial neighborhood
        k_s = self.nbh_s
        k_t = self.nbh_t

        # check if we want to iterate the temporal domain with the same nbh as the spatial domain
        if cubic:
            k_t = k_s

        # determine number of lsci images that will be calculated
        # from the image stack over the temporal neighborhood
        n = int(stack_size / k_t)

        # create array for lsci images that will be caluclated,
        # size n is depending on the temporal neighborhood
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
                    st_lsci[x, w, h] = self.calc_array_contrast(cuboid)

        return np.mean(st_lsci, axis=0)
