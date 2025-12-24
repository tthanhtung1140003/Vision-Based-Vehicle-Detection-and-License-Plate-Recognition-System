from ultralytics import YOLO

def detect_licensePlate(license_plate_img):
    license_plate_model = YOLO(r'license_plate_detector.pt')
    results_license_plate = license_plate_model.predict(license_plate_img)

    for result in results_license_plate:
        boxes_lp = result.boxes
        for box_lp in boxes_lp:
            x1_lp, y1_lp, x2_lp, y2_lp = map(int, box_lp.xyxy[0])  
            cropped_licenseP = license_plate_img[y1_lp:y2_lp, x1_lp:x2_lp]
            return cropped_licenseP 
    return None
