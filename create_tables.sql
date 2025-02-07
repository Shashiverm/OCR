CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    UNIQUE (name, dob)
);

CREATE INDEX idx_patients_name_dob ON patients (name, dob);

CREATE TABLE forms_data (
    id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(id),
    form_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_forms_data_patient_id ON forms_data (patient_id);
CREATE INDEX idx_forms_data_created_at ON forms_data (created_at);

