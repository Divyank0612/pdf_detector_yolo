from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image, ImageDraw

def pdf_to_images(pdf_path, output_folder, dpi=200):
    """Convert PDF pages to images"""
    output_folder = Path(output_folder)
    images = convert_from_path(pdf_path, dpi=dpi)   
    img_paths = []
    for i, img in enumerate(images):
        img_name = output_folder / f"{pdf_path.stem}_page{i}.jpg"
        img.save(img_name, "JPEG")
        img_paths.append(img_name)
    return img_paths

def annotate_image(img_path, boxes, save_path):
    """Draw bounding boxes on image"""
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    for box in boxes:
        xyxy = box['bbox']
        label = box['class']
        draw.rectangle(xyxy, outline="red", width=3)
        draw.text((xyxy[0], xyxy[1]-10), label, fill="red")
    img.save(save_path)

def map_yolo_to_pdf(xyxy, img_width, img_height, pdf_width, pdf_height):
    """Map YOLO normalized coordinates back to PDF coordinates"""
    x0, y0, x1, y1 = xyxy
    scale_x = pdf_width / img_width
    scale_y = pdf_height / img_height
    return [
        x0 * scale_x,
        y0 * scale_y,
        x1 * scale_x,
        y1 * scale_y
    ]
