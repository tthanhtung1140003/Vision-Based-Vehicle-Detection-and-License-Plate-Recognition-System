import easyocr
import re
import cv2

reader = easyocr.Reader(['en'], gpu=False)  

def OCR(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(image)

    results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))

    text_output = ""
    for (bbox, text, prob) in results:
        text_output += text + " "  

    text_output = text_output.strip().upper()  
    text_output = re.sub(r'\s+', '', text_output)  
    text_output = re.sub(r'[^A-Z0-9]', '', text_output)  

    return text_output  
