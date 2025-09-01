# PDF Entity Detection Pipeline – Stage 1 (YOLOv8)

This project implements a **PDF entity detection pipeline** using **YOLOv8**. It focuses on detecting and classifying entities in digital PDFs, such as:

- **Headers**  
- **Tables**  
- **Text**  
- **Figures**  
- **Equations**  
- **Charts**  
- **Footers**  

> ⚠️ Stage 1 is focused on **detection only**. No content extraction is performed.  

---

## 🎯 Objective

The primary objectives of Stage 1 are:

1. Accurately detect layout entities in PDFs.  
2. Generate **annotated PDFs**, **JSON results**, and **visual preview images**.  
3. Establish a foundation for **Stage 2**, aiming for near **100% detection accuracy**.

---

## 🛠 Technologies & Tools

| Component | Purpose |
|-----------|---------|
| **Python 3.9** | Main programming language. |
| **YOLOv8s (pre-trained)** | Lightweight object detection model for layout entity detection. |
| **PyMuPDF (fitz)** | Manipulating PDFs and drawing bounding boxes. |
| **PIL / Pillow** | Image processing (PDF to image conversion). |
| **Ultralytics YOLO library** | YOLOv8 model APIs for inference. |
| **JSON** | Structured storage of detection results. |
| **Conda** | Environment management for reproducibility. |

---

## 📁 Project Structure

doclaynet-yolo/
├── data/
│ └── my_pdfs/ # Sample PDFs for testing
├── outputs/
│ ├── annotated_pdfs/ # PDFs with detected bounding boxes
│ ├── predictions/ # Annotated images
│ └── json/ # Detection results in JSON format
├── scripts/
│ ├── infer.py # Main inference script
│ ├── utils.py # Helper functions
│ └── gpu_check.py # Verify GPU/CPU setup
├── weights/ # Pre-trained YOLOv8 model weights
├── requirements.txt # Python dependencies
└── README.md


---

## ⚙️ Setup Instructions

1. **Clone the repository**

git clone https://github.com/yourusername/pdf_detector_yolo.git
cd pdf_detector_yolo
Create and activate the Conda environment



conda create -n pdf_detector_yolo python=3.10 -y
conda activate pdf_detector_yolo
pip install -r requirements.txt
Verify GPU/CPU availability


python scripts/gpu_check.py
🚀 Usage
Place PDFs in the folder:



data/my_pdfs/
Run inference:



python -m scripts.infer
Check outputs:

outputs/annotated_pdfs/ → Annotated PDFs

outputs/predictions/ → Annotated images per PDF page

outputs/json/ → JSON with detection results (labels, bounding boxes, confidence scores)

📌 Notes
Stage 1 uses YOLOv8s for fast prototyping.

Large datasets and model weights are not included due to size. Download DocLayNet manually if needed.

.gitignore excludes large datasets, model weights, and outputs. Only sample PDFs and scripts are committed.

🏗 Stage 2 Plan
Upgrade detection model to PP-YOLOE-S for improved accuracy.

Aim for 100% entity classification accuracy.

Optimize inference for GPU and improve annotated PDF outputs.

Potentially include post-processing to reduce false positives and overlaps.

📜 References
YOLOv8 Documentation

DocLayNet Dataset

PyMuPDF Documentation


