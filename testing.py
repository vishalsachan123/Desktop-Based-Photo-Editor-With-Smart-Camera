#import PIL and numpy 
from PIL import Image
import numpy as np
# open images by providing path of images
img1 = Image.open("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo.jpg") 
img2 = Image.open("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo2.jpg")
img3 = Image.open("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo.jpg")
img4 = Image.open("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo1.jpg")
#create arrays of above images
img1_array = np.array(img1)
img2_array = np.array(img2)
img3_array = np.array(img3)
img4_array = np.array(img4)
# ====== collage of 2 images ====== 
# arrange arrays of two images in a single row 
imgg = np.hstack([img1_array , img2_array]) 
#create image of imgg array
finalimg = Image.fromarray(imgg)
#provide the path with name for finalimg where you want to save it
finalimg.save("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo1.jpg")
print("First image saved")
# ====== collage of 4 images ====== 
# arrange arrays of four images in two rows
imgg1 = np.vstack([np.hstack([img1_array , img2_array]) , np.hstack([img3_array , img4_array])]) 
#create image of imgg1 array
finalimg1 = Image.fromarray(imgg1)
#provide the path with name for finalimg1 where you want to save it
finalimg1.save("C:/Users/HP/Desktop/TYProject(ImageEditor)/Desktop Based Photo Editor/demo2.jpg")
print("Second image saved")