from matplotlib import pyplot as plt
from pylsci.lsci import Lsci
from util import stack_images

# TODO
#   - demo notebook
#   - contact author for permission to use image and verification of code


def show_image(img):
    plt.imshow(img)
    plt.colorbar()
    plt.show()


lsci = Lsci()
# lsci.nbh_s = 4
# lsci.nbh_s = 5

print('temporal LSCI ...')
speckle_imgs = plt.imread('img/temporal.png')
speckle_img_stack = stack_images(speckle_imgs)
print(speckle_img_stack.shape)
t_lsci = lsci.temporal_contrast(speckle_img_stack)
show_image(t_lsci)
print(t_lsci.shape)

print('spatio-temporal LSCI ...')
speckle_imgs = plt.imread('img/temporal.png')
speckle_img_stack = stack_images(speckle_imgs)
print(speckle_img_stack.shape)
st_lsci = lsci.spatio_temporal_contrast(speckle_img_stack)
show_image(st_lsci)
print(st_lsci.shape)

print('spatial LSCI ...')
speckle_img = plt.imread('img/spatial.tif')
print(speckle_img.shape)
s_lsci = lsci.spatial_contrast(speckle_img)
show_image(s_lsci)
print(s_lsci.shape)

print('success')

