import cv2
import numpy as np

def resize(image):
    height, width = image.shape[:2]
    original_area = height * width
    target_area = 250000
    scale_factor = (target_area / original_area) ** 0.5  
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image

def extract_license_plate(image):
    #image = resize(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5, 0)
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edges = cv2.Canny(binary_image, 50, 150)
    #cv2.imshow('binary', binary_image)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] 

    for contour in largest_contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.06 * peri, True)
        
        if len(approx) == 4:  
            (tl, tr, br, bl) = approx.reshape(4, 2)
            angle_deg = np.degrees(np.arctan2(tr[1] - tl[1], tr[0] - tl[0])) % 360
            [x, y, w, h] = cv2.boundingRect(approx)
            ratio = w / h
            area_ratio = cv2.contourArea(approx) / (w * h)

            if (1 <= ratio <= 10) and area_ratio > 0.5 and (250 <= angle_deg <= 290 or 60 <= angle_deg <= 120):
                #cv2.drawContours(image, [approx], -1, (0, 0, 255), 3)  # Đường bao

                pts = approx.reshape(4, 2)
                rect = np.zeros((4, 2), dtype="float32")
                rect[0] = pts[np.argmin(pts.sum(axis=1))]  
                rect[2] = pts[np.argmax(pts.sum(axis=1))]  
                rect[1] = pts[np.argmin(np.diff(pts, axis=1))]  
                rect[3] = pts[np.argmax(np.diff(pts, axis=1))]  

                width = max(np.linalg.norm(rect[1] - rect[0]), np.linalg.norm(rect[2] - rect[3]))
                height = max(np.linalg.norm(rect[3] - rect[0]), np.linalg.norm(rect[2] - rect[1]))

                dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(image, M, (int(width), int(height)))

                return warped  
    return None  
