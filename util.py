import functools
import time
import numpy as np


def time_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        x = func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"run time: {start - finish}")
        return x
    return wrapper


def stack_images(data_2D):
    """
    Stacks the vertically aligned 1000 raw laser speckle images (2D data) to a cuboid of 1000 laser speckle images (3D data).
    :param data_2D: Input data as provided by the sensor, that is 1000 vertically aligned raw laser speckle images. Size should be 64000x64
    :return: data_3D: 1000 laser speckle images stacked to 3D data (cuboid of 1000 raw laser speckle images). Size should be 1000x64x64.
    """

    # width, height
    w, h = data_2D.shape
    # get number of vertically aligned images, should be 1000
    n = int(w / h)

    # create 3D array of shape n x w x h, should be 1000 x 64 x 64
    data_3D = np.zeros([n, h, h])  # , dtype='uint8'

    for i in range(0, n):
        # data_3D[i,:,:] = stripe[i*h:i*h+h,:]
        # use h to iterate through the vertical aligned images.
        # always move h pixels in vertical direction. h should be 64
        data_3D[i, :, :] = data_2D[i * h:i * h + h, :]

    return data_3D


# def stack_images(stripe: np.ndarray) -> np.ndarray:
#     # rows, columns
#     rows, cols = stripe.shape
#     # get number of vertically aligned images
#     n = int(rows / cols)
#
#     # create 3D array of shape n x w x h, should be 1000 x 64 x 64
#     stack = np.zeros([n, cols, cols], dtype='uint8')
#
#     for i in range(0, n):
#         from_row = i * cols
#         to_row = i * cols + cols
#         stack[i, :, :] = stripe[from_row:to_row, :]
#
#     return stack
