import cv2

filename = "img.jpg"

imgColor = cv2.imread(filename, cv2.IMREAD_COLOR)
imgGray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

cv2.imshow("Color", imgColor)
cv2.imshow("GrayScale", imgGray)

cv2.waitKey(10000)
cv2.destroyAllWindows()