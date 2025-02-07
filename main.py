import os
import logging
from ocr_module import extract_text_from_image
from json_converter import convert_to_json
from db_module import insert_data_to_db

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_form(image_path):
    try:
        # Check if the image file exists
        if not os.path.exists(image_path):
            logging.error(f"Image file does not exist: {image_path}")
            return
        
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        # Check if the extracted text is empty
        if not extracted_text:
            logging.error(f"Failed to extract text from image: {image_path}")
            return
        
        # Convert extracted text to JSON
        json_data = convert_to_json(extracted_text)
        
        # Insert JSON data into the database
        insert_data_to_db(json_data)
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")

def main():
    # Directory containing the form images
    forms_directory = "patient_forms"
    
    if not os.path.exists(forms_directory):
        logging.error(f"Directory not found: {forms_directory}")
        return
    
    # Process all images in the directory
    for filename in os.listdir(forms_directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
            image_path = os.path.join(forms_directory, filename)
            process_form(image_path)

if __name__ == "__main__":
    main()

