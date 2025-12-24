import cv2
from plate_detect import plate_process


img_path = r"...."
input_img = cv2.imread(img_path)
img4=cv2.resize(input_img,(1280,720))
cv2.imshow("input",img4)
img,img2,text = plate_process(input_img)
print (text)

cv2.waitKey (0)
