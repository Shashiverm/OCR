import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging
from pdf2image import convert_from_path
import os

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        logging.error(f"Failed to load image: {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((1, 1), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return Image.fromarray(thresh)

def extract_text_from_image(image_path):
    try:
        extracted_text = ""
        
        # Handle PDFs
        if image_path.lower().endswith(".pdf"):
            images = convert_from_path(image_path)
            for i, image in enumerate(images):
                temp_image_path = f"temp_page_{i}.png"
                image.save(temp_image_path, "PNG")

                # Process image and extract text
                preprocessed_image = preprocess_image(temp_image_path)
                if preprocessed_image:
                    extracted_text += pytesseract.image_to_string(preprocessed_image)

                # Clean up temp image
                os.remove(temp_image_path)
        else:
            # Process image files
            preprocessed_image = preprocess_image(image_path)
            if preprocessed_image:
                extracted_text = pytesseract.image_to_string(preprocessed_image)

        return extracted_text
    except Exception as e:
        logging.error(f"Error in OCR process: {str(e)}")
        return None
