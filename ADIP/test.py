import cv2
import numpy as np
# Read the images
foreground = cv2.imread("./DataMask/original/man-person-jumping-desert.png")
background = cv2.imread("./PyFile/pic_412_8.jpg")
alpha = cv2.imread("./DataMask/label/man-person-jumping-desert.png")
background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]), 
                                interpolation=cv2.INTER_CUBIC)
 
# Convert uint8 to float
foreground = foreground.astype(float)
background = background.astype(float)
 
# Normalize the alpha mask to keep intensity between 0 and 1
alpha = alpha.astype(float)/255
 
# Multiply the foreground with the alpha matte
foreground = cv2.multiply(alpha, foreground)
 
# Multiply the background with ( 1 - alpha )
background = cv2.multiply(1.0 - alpha, background)
 
# Add the masked foreground and background.
outImage = cv2.add(foreground, background)

outImage = outImage/255
saveImg = np.zeros((foreground.shape[0], foreground.shape[1], 3))
cv2.normalize(outImage, saveImg, 0, 255, cv2.NORM_MINMAX)
print(saveImg)

# Display image
cv2.imshow('tt',outImage)
cv2.moveWindow("tt",1000,100)
# cv2.imwrite('tt.png', outImage)
cv2.waitKey(0)
# cv2.imshow("outImg", outImage/255)
# cv2.waitKey(0)