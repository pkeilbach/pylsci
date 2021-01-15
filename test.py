from matplotlib import pyplot as plt
import numpy as np
from pylsci.lsci import Lsci
from util import stack_images


def show_image(img):
    plt.imshow(img)
    plt.colorbar()
    plt.show()


lsci = Lsci()

bf = plt.imread('test/bf.png')
# bf_scaled = ((bf - bf.min()) * 255) / (bf.max() - bf.min())
# bf_scaled = bf_scaled.astype(int)
bf_3d = stack_images(bf)
contrast_img_t = lsci.get_temporal_contrast_img(bf_3d)
print(contrast_img_t.shape)
show_image(contrast_img_t)


print('hello pylsci')
speckle_img = plt.imread('test/spatial.tif')
print(speckle_img.shape)
show_image(speckle_img)


# print('running vectorized ...')
# contrast_img_vec = lsci.get_spatial_contrast_img(speckle_img, vectorized=True)
# show_image(contrast_img_vec)
# # print(contrast_img.shape)
#
# print('running non-vectorized ...')
# contrast_img = lsci.get_spatial_contrast_img(speckle_img, vectorized=False)
# show_image(contrast_img)

print('success')

