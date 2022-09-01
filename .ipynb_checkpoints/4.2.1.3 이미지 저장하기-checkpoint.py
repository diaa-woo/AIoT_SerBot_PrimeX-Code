import cv2

imgOrigin = cv2.imread("img.jpg", cv2.IMREAD_COLOR)

b, g, r = cv2.split(imgOrigin)
imgNew = cv2.merge([r, g, b])

cv2.imshow("Origin", imgOrigin)
cv2.imshow("New", imgNew)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("new_img.jpg", imgNew)