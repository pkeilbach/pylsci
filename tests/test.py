from pylsci import Lsci
from util import stack_images, show_image, read_image

lsci = Lsci()

print("temporal LSCI ...")
speckle_imgs = read_image("img/temporal.png")
speckle_img_stack = stack_images(speckle_imgs)
print(speckle_img_stack.shape)
t_lsci = lsci.temporal_contrast(speckle_img_stack)
show_image(t_lsci)
print(t_lsci.shape)

print("spatio-temporal LSCI ...")
speckle_imgs = read_image("img/temporal.png")
speckle_img_stack = stack_images(speckle_imgs)
print(speckle_img_stack.shape)
st_lsci = lsci.spatio_temporal_contrast(speckle_img_stack)
show_image(st_lsci)
print(st_lsci.shape)

print("spatial LSCI ...")
speckle_img = read_image("img/spatial.tif")
print(speckle_img.shape)
s_lsci = lsci.spatial_contrast(speckle_img)
show_image(s_lsci)
print(s_lsci.shape)

print("success")
