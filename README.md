# Vision-Based Vehicle Detection and License Plate Recognition System

**Language:** Python

---

## Overview

This repository presents a vision-based system for vehicle detection and automatic license plate recognition (LPR) using deep learning and classical computer vision techniques. The system is designed for intelligent traffic monitoring, smart parking, and access control applications.

The pipeline processes images or video streams to detect vehicles, localize license plates, recognize plate text, and generate annotated outputs with structured results.

The project emphasizes **system-level integration**, **real-time inference**, and **data privacy awareness**, rather than isolated model performance.

---

## Key Features

- **Vehicle Detection**
  - Real-time detection of cars, motorcycles, buses, and trucks
  - Based on YOLOv8 (Ultralytics)

- **License Plate Recognition**
  - Optical character recognition using EasyOCR
  - Optimized for Vietnamese and international license plate formats

- **End-to-End Pipeline**
  - Image / video input → detection → plate crop → OCR → visualization
  - Modular architecture for easy extension and replacement

- **Deployment-Oriented**
  - Supports CPU and GPU inference
  - Suitable for edge devices (e.g., Raspberry Pi, Jetson)

- **Privacy-Aware Design**
  - No sensitive raw data included
  - Demonstrations rely on public or anonymized datasets only

---

## Motivation

In urban traffic management and secure access systems, manual license plate inspection is inefficient and error-prone. This project explores how modern computer vision pipelines can automate vehicle identification while remaining compatible with real-world constraints such as limited computational resources and data protection regulations.

---

## System Architecture

The system follows a modular processing pipeline:

Input Image / Video  
↓  
Vehicle Detection (YOLOv8)  
↓  
Vehicle ROI Selection  
↓  
License Plate Localization  
↓  
Image Preprocessing & Warping  
↓  
OCR Recognition (EasyOCR)  
↓  
Post-processing & Validation  
↓  
Annotated Output + Structured Results  

### Processing Stages

1. **Input Processing**
   - Load images or video streams using OpenCV

2. **Vehicle Detection**
   - YOLOv8 detects vehicles with confidence thresholding

3. **Plate Localization**
   - License plate region extraction from detected vehicles

4. **OCR Recognition**
   - Grayscale conversion, denoising, and text extraction

5. **Post-Processing**
   - Confidence filtering
   - License plate format validation (rule-based)

---

## Models

- **Vehicle Detection**
  - YOLOv8 (nano / small variants for real-time performance)
  - Pre-trained weights with internal fine-tuning

- **OCR**
  - EasyOCR with Vietnamese language support

---

## Technology Stack

- Python 3.8+
- PyTorch
- OpenCV
- Ultralytics YOLOv8
- EasyOCR
- NumPy, Matplotlib
- Qt (optional visualization modules)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- GPU recommended (CUDA-supported), but not required

### Setup
```bash
git clone https://github.com/thanhtung1140003/Vision-Based-Vehicle-Detection-and-License-Plate-Recognition-System.git
cd Vision-Based-Vehicle-Detection-and-License-Plate-Recognition-System
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Image Inference
```bash
python src/inference.py \
  --input_path data/samples/sample.jpg \
  --output_dir results/
```
Outputs:
- Annotated image with bounding boxes and recognized text
- JSON file containing plate text and confidence scores

### Video / Webcam Processing
```bash
python src/main.py \
  --source videos/sample.mp4 \
  --conf 0.5
```
- Use `--source 0` for webcam input
- Adjustable detection confidence threshold

---

## Results (Indicative)

Evaluation was conducted using a combination of public datasets and anonymized internal data.

| Metric          | Public Datasets | Internal Evaluation |
|-----------------|-----------------|---------------------|
| Detection mAP@0.5 | ~0.88          | ~0.92              |
| LPR Accuracy    | ~0.82          | ~0.87              |
| FPS (GPU)       | ~25            | ~30                |
| FPS (CPU)       | ~10            | ~15                |

Performance varies depending on lighting conditions, camera quality, and vehicle speed.

---

## Data Privacy & Legal Notice

- Training datasets and custom-trained model weights are not included
- Some data were provided by external organizations under confidentiality agreements
- To comply with data protection regulations, this repository contains:
  - Source code only
  - Public or synthetic demo data
  - No personally identifiable information (PII)
- All example runs in this repository rely exclusively on public or anonymized datasets.

---

## Limitations

- Reduced accuracy under heavy occlusion or adverse weather
- OCR performance degrades with motion blur or severe perspective distortion
- Currently optimized primarily for Vietnamese license plate formats

---

## Future Work

- Dedicated license plate detector (two-stage detection pipeline)
- Transformer-based OCR models
- Multi-country license plate support
- Edge optimization using ONNX / TensorRT
- Integration with intelligent transportation systems

---

## Author

Thanh Tung Nguyen  
Mechatronics Engineering  
Computer Vision & Intelligent Systems  
GitHub: https://github.com/thanhtung1140003

---

## License

Models / Data: Not included (restricted or proprietary).

---

## References

- Ultralytics YOLOv8
- EasyOCR
- CCPD Dataset
- IEEE: Federated Learning for Edge Computing (2023)

---

Last updated: December 23, 2025
