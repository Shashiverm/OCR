import psycopg2
import json
# import mysql.connector
import logging
from psycopg2.extras import Json

def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="ocrdb",
            user="ocr",
            password="",
            host="localhost",
            port="5432"
        )
    except psycopg2.Error as e:
        logging.error(f"Unable to connect to the database: {e}")
        raise

def insert_data_to_db(json_data):
    if not json_data:
        logging.error("Received NoneType JSON data. Skipping insertion.")
        return
    
    conn = None
    cur = None
    try:
        data = json.loads(json_data)

        if not data.get("patient_name") or not data.get("dob"):
            logging.error(f"Missing critical patient data in JSON: {json_data}")
            return

        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO patients (name, dob)
            VALUES (%s, %s)
            ON CONFLICT (name, dob) DO NOTHING
            RETURNING id
        """, (data["patient_name"], data["dob"]))

        patient_id = cur.fetchone()

        if not patient_id:
            cur.execute("SELECT id FROM patients WHERE name = %s AND dob = %s", (data["patient_name"], data["dob"]))
            patient_id = cur.fetchone()

        if not patient_id:
            logging.error("Failed to retrieve patient ID. Skipping form insertion.")
            return

        # Insert form data
        cur.execute("""
            INSERT INTO forms_data (patient_id, form_json)
            VALUES (%s, %s)
        """, (patient_id[0], json_data))

        conn.commit()
        logging.info(f"Data inserted successfully for patient: {data['patient_name']}")

    except (psycopg2.Error, json.JSONDecodeError, ValueError) as e:
        logging.error(f"Error inserting data into the database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
