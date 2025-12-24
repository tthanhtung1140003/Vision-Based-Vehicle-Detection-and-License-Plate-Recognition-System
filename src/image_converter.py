# image_converter.py
import cv2
from PySide6.QtGui import QPixmap, QImage

def convert_image_to_pixmap(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    height, width, channel = image_rgb.shape
    bytes_per_line = 3 * width
    q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image) 
