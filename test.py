from matplotlib import pyplot as plt
import numpy as np
from pylsci.lsci import Lsci


def show_image(img):
    plt.imshow(img)
    plt.colorbar()
    plt.show()


print('hello pylsci')
speckle_img = plt.imread('test/spatial.tif')
print(speckle_img.shape)
show_image(speckle_img)

lsci = Lsci()

print('running vectorized ...')
contrast_img_vec = lsci.get_spatial_contrast_img(speckle_img, vectorized=True)
show_image(contrast_img_vec)
# print(contrast_img.shape)

print('running non-vectorized ...')
contrast_img = lsci.get_spatial_contrast_img(speckle_img, vectorized=False)
show_image(contrast_img)

print('success')

