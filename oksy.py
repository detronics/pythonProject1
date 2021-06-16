import pytesseract
import cv2

x = 235
y = 120
h = 105
w = 90
img = cv2.imread("oks11.jpg")
crop_img = img[y:y+h, x:x+w]
rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
resize_img = cv2.resize(rgb, None, fx=9, fy=9)
finall = cv2.bitwise_not(resize_img)
config = r'--oem 3 --psm 6'
saturation = pytesseract.image_to_string(finall, config=config)[:-2]
print(saturation)


