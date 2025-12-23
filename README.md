

```markdown
# Vision-Based Vehicle Detection and License Plate Recognition System

**Language:** Python  
**License:** MIT (Code only)  
**Focus:** Computer Vision · Intelligent Transportation · Ethical AI  

---

## Overview

This repository presents a vision-based system for vehicle detection and automatic license plate recognition (LPR) using deep learning and classical computer vision techniques. The system is designed for intelligent traffic monitoring, smart parking, and access control applications.

The pipeline processes images or video streams to:
- Detect vehicles
- Localize license plates
- Recognize plate text
- Produce annotated visual outputs and structured results

The project emphasizes **system-level integration**, **real-time inference**, and **data privacy awareness**, rather than isolated model performance.

---

## Key Features

- **Vehicle Detection**
  - Real-time detection of cars, motorcycles, buses, and trucks
  - Based on YOLOv8 (Ultralytics)

- **License Plate Recognition**
  - OCR using EasyOCR
  - Optimized for Vietnamese and international plate formats

- **End-to-End Pipeline**
  - Image / video input → detection → plate crop → OCR → visualization
  - Modular design for easy replacement of components

- **Deployment-Oriented**
  - Runs on CPU and GPU
  - Suitable for edge devices (e.g., Raspberry Pi, Jetson)

- **Privacy-Aware Design**
  - No raw sensitive data included
  - Public demos use open or anonymized datasets only

---

## Motivation

In urban traffic management and secure access systems, manual license plate inspection is inefficient and error-prone. This project explores how modern computer vision pipelines can automate vehicle identification while remaining compatible with real-world constraints such as limited hardware resources and data protection regulations.

---

## System Architecture

The system follows a modular processing pipeline:

```

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

````

### Processing Stages

1. **Input Processing**
   - Load images or video streams using OpenCV

2. **Vehicle Detection**
   - YOLOv8 detects vehicles with confidence filtering

3. **Plate Localization**
   - Sub-region extraction inside detected vehicle bounding boxes

4. **OCR Recognition**
   - Grayscale conversion, denoising, and text extraction

5. **Post-Processing**
   - Confidence thresholding
   - Plate format validation (regex-based)

---

## Models

- **Vehicle Detection**
  - YOLOv8 (nano / small variants for speed)
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
- Qt (for visualization modules, if enabled)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- GPU recommended (CUDA-compatible), but not required

### Setup

```bash
git clone https://github.com/thanhtung1140003/Vision-Based-Vehicle-Detection-and-License-Plate-Recognition-System.git
cd Vision-Based-Vehicle-Detection-and-License-Plate-Recognition-System

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
````

---

## Usage

### Image Inference

```bash
python src/inference.py \
  --input_path data/samples/sample.jpg \
  --output_dir results/
```

Outputs:

* Annotated image
* JSON file with recognized plate text and confidence scores

### Video / Webcam Processing

```bash
python src/main.py \
  --source videos/sample.mp4 \
  --conf 0.5
```

* Use `--source 0` for webcam input
* Adjustable confidence threshold

---

## Results (Indicative)

Evaluation was conducted on a combination of public datasets and anonymized internal data.

| Metric            | Public Datasets | Internal Evaluation |
| ----------------- | --------------- | ------------------- |
| Detection mAP@0.5 | ~0.88           | ~0.92               |
| LPR Accuracy      | ~0.82           | ~0.87               |
| FPS (GPU)         | ~25             | ~30                 |
| FPS (CPU)         | ~10             | ~15                 |

> Note: Results depend on camera quality, lighting conditions, and plate visibility.

---

## Data Privacy & Legal Notice

* **Training data and custom model weights are NOT included**
* Some datasets were provided by external organizations under confidentiality agreements
* To comply with data protection regulations, the repository includes:

  * Code only
  * Public or synthetic demo data
  * No identifiable personal information (PII)

All examples in this repository use **public or anonymized data only**.

---

## Limitations

* Performance degrades under heavy occlusion or poor weather
* OCR accuracy is lower for blurred or tilted plates
* Currently optimized mainly for Vietnamese plate formats

---

## Future Work

* Dedicated license plate detector (two-stage pipeline)
* Transformer-based OCR models
* Multi-country plate support
* Edge optimization (TensorRT / ONNX)
* Integration with smart city platforms

---

## Ethical AI Statement

This project is intended strictly for **research and educational purposes**. Any real-world deployment must comply with local laws, privacy regulations, and ethical guidelines for computer vision systems.

---

## Author

**Thanh Tung Nguyen**
Mechatronics Engineering
Computer Vision & Intelligent Systems

GitHub: [https://github.com/thanhtung1140003](https://github.com/thanhtung1140003)

---

## License

* **Code:** MIT License
* **Models / Data:** Not included (restricted or proprietary)

---

## References

* Ultralytics YOLOv8
* EasyOCR
* CCPD Dataset
* IEEE: Federated Learning for Edge Computing (2023)

*Last updated: December 2025*
