# Patient Assessment Form OCR

This project automates the extraction of data from patient assessment forms using Optical Character Recognition (OCR) and stores the extracted data in a PostgreSQL database.

## Features

- Extracts text from image files (JPEG, PNG, PDF) using Tesseract OCR
- Processes both handwritten and printed text
- Converts extracted data into a structured JSON format
- Stores patient information and form data in a PostgreSQL database
- Handles errors and provides logging for better debugging

## Prerequisites

- Python 3.7+
- PostgreSQL database
- Tesseract OCR

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/Shashiverm/OCR.git
   cd patient-assessment-ocr
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR:
   - On Windows: Download and install from [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - On Linux/macOS:
     ```sh
     sudo apt install tesseract-ocr  # Ubuntu/Debian
     brew install tesseract  # macOS
     ```

5. Configure PostgreSQL database:
   - Create a database:
     ```sql
     CREATE DATABASE patient_ocr_db;
     ```
   - Update `config.py` with your database credentials:
     ```python
     DATABASE_CONFIG = {
         'dbname': 'patient_ocr_db',
         'user': 'your_username',
         'password': 'your_password',
         'host': 'localhost',
         'port': 5432
     }
     ```

## Usage

1. Run the script to process an image or PDF:
   ```sh
   python main.py --file path/to/your/image_or_pdf
   ```

2. The extracted data will be stored in the PostgreSQL database.

3. View logs for debugging:
   ```sh
   cat logs/app.log
   ```

## Folder Structure
```
patient-assessment-ocr/
├── data/                 # Sample images and PDFs
├── logs/                 # Logs for debugging
├── models/               # Database models and schema
├── scripts/              # Utility scripts
├── main.py               # Main script to process OCR
├── config.py             # Configuration file for database
├── requirements.txt      # Required dependencies
├── README.md             # Project documentation
```

## Contributing

Contributions are welcome! Please follow these steps:
- Fork the repository
- Create a new branch 
- Commit your changes
- Open a pull request




