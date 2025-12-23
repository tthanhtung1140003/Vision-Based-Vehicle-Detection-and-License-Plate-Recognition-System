from ultralytics import YOLO

from warpingplate import extract_license_plate
from detect_licensePlate import detect_licensePlate 
from OCR import OCR

model = YOLO(r"x.pt")
classNames = ["person", "bicycle", "car", "motorbike", "bus", "truck"]

def plate_process(img):
    if img is None:
        print("Không thể đọc ảnh.")
    else:
        max_area = 0
        best_cropped_img = None

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])  

                if cls < len(classNames) and (classNames[cls] == "car" or classNames[cls] == "motorbike"):
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        area = (x2 - x1) * (y2 - y1)

                        if area > max_area:
                            max_area = area
                            best_cropped_img = img[y1:y2, x1:x2]
    
        if best_cropped_img is not None:
            cropped_license_plate = detect_licensePlate(best_cropped_img)
            if cropped_license_plate is not None:
                licensePlate = extract_license_plate(cropped_license_plate)
                recognized_text = OCR(cropped_license_plate)
            # cv2.imshow("Best cropped",best_cropped_img)
            # cv2.imshow("license p",cropped_license_plate)
                print(recognized_text)

            if licensePlate is not None:
                return best_cropped_img, licensePlate, recognized_text
            if licensePlate is None:
                return best_cropped_img, cropped_license_plate, recognized_text

        return None, None, ""  



