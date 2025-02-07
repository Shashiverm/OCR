import json
import re
import logging

def clean_extracted_text(text):
    """ Cleans extracted text by removing excessive whitespace and newlines. """
    return ' '.join(text.split())

def extract_field(text, field_name):
    pattern = rf"{re.escape(field_name)}:?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None

def extract_difficulty_ratings(text):
    difficulties = ["bending", "putting on shoes", "sleeping"]
    ratings = {}
    for difficulty in difficulties:
        rating = extract_field(text, difficulty)
        if rating and rating.isdigit():
            ratings[difficulty] = int(rating)
    return ratings

def extract_pain_symptoms(text):
    symptoms = ["pain", "numbness", "tingling", "burning", "tightness"]
    ratings = {}
    for symptom in symptoms:
        rating = extract_field(text, symptom)
        if rating and rating.isdigit():
            ratings[symptom] = int(rating)
    return ratings

def extract_medical_assistant_data(text):
    fields = ["blood pressure", "hr", "weight", "height", "spo2", "temperature", "blood glucose", "respirations"]
    data = {}
    for field in fields:
        value = extract_field(text, field)
        if value:
            data[field.replace(" ", "_")] = value
    return data

def convert_to_json(extracted_text):
    try:
        extracted_text = clean_extracted_text(extracted_text)
        logging.info(f"Extracted Text for JSON Conversion:\n{extracted_text}")
        # Extract basic patient information with stricter validation
        name_match = re.search(r"Patient Name:\s*([A-Za-z\s]+)", extracted_text)
        dob_match = re.search(r"Date of Birth[\s:]*([\d]{4}-[\d]{2}-[\d]{2})", extracted_text, re.IGNORECASE)
        date_match = re.search(r"Date:\s*([\d]{4}-[\d]{2}-[\d]{2})", extracted_text)

        # Validate DOB first
        if not dob_match:
            raise ValueError("Date of birth is missing")

        data = {
            "patient_name": name_match.group(1).strip() if name_match else None,
            "dob": dob_match.group(1).strip(),
            "date": date_match.group(1).strip() if date_match else None,
            "injection": extract_field(extracted_text, "injection"),
            "exercise_therapy": extract_field(extracted_text, "exercise therapy"),
            "difficulty_ratings": extract_difficulty_ratings(extracted_text),
            "patient_changes": {
                "since_last_treatment": extract_field(extracted_text, "since last treatment"),
                "since_start_of_treatment": extract_field(extracted_text, "since start of treatment"),
                "last_3_days": extract_field(extracted_text, "last 3 days")
            },
            "pain_symptoms": extract_pain_symptoms(extracted_text),
            "medical_assistant_data": extract_medical_assistant_data(extracted_text)
        }
        
        # Clean any None values
        data = {k: v for k, v in data.items() if v is not None}
        
        return json.dumps(data)
    except Exception as e:
        logging.error(f"Error in JSON conversion: {str(e)}")
        return None
