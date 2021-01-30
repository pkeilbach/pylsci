import functools
import time
from matplotlib import pyplot as plt
import numpy as np


def read_image(path):
    return plt.imread(path)


def show_image(img):
    print(f"image dimensions: {img.shape}")
    plt.imshow(img)
    plt.colorbar()
    plt.show()


def time_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        x = func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"run time: {start - finish}")
        return x
    return wrapper


def stack_images(img_stripe):
    # width, height
    w, h = img_stripe.shape
    # get number of vertically aligned images
    n = int(w / h)
    # create 3D array of shape n x w x h
    img_stack = np.zeros([n, h, h])

    for i in range(0, n):
        # data_3D[i,:,:] = stripe[i*h:i*h+h,:]
        # use h to iterate through the vertical aligned images.
        # always move h pixels in vertical direction.
        from_row = i * h
        to_row = i * h + h
        img_stack[i, :, :] = img_stripe[from_row:to_row, :]

    return img_stack
