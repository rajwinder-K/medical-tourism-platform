import sqlite3
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_NAME = "medical_tourism.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    # Return rows like dictionaries
    connection.row_factory = sqlite3.Row

    # Enable foreign-key relationships
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# HOSPITAL FUNCTIONS
# ============================================================

def get_hospitals():
    """
    Return all hospitals.
    """

    connection = get_connection()

    try:

        hospitals = connection.execute("""
            SELECT
                id,
                name,
                city,
                specialty,
                rating,
                beds,
                description,
                facilities
            FROM hospitals
            ORDER BY name
        """).fetchall()

        return [dict(hospital) for hospital in hospitals]

    finally:

        connection.close()


def get_hospital_by_id(hospital_id):
    """
    Return one hospital using its ID.
    """

    connection = get_connection()

    try:

        hospital = connection.execute("""
            SELECT
                id,
                name,
                city,
                specialty,
                rating,
                beds,
                description,
                facilities
            FROM hospitals
            WHERE id = ?
        """, (hospital_id,)).fetchone()

        if hospital is None:
            return None

        return dict(hospital)

    finally:

        connection.close()


# ============================================================
# TREATMENT FUNCTIONS
# ============================================================

def get_treatments():
    """
    Return all treatments.
    """

    connection = get_connection()

    try:

        treatments = connection.execute("""
            SELECT
                id,
                name,
                category,
                description,
                duration,
                estimated_cost
            FROM treatments
            ORDER BY name
        """).fetchall()

        return [dict(treatment) for treatment in treatments]

    finally:

        connection.close()


def get_treatment_by_id(treatment_id):
    """
    Return one treatment using its ID.
    """

    connection = get_connection()

    try:

        treatment = connection.execute("""
            SELECT
                id,
                name,
                category,
                description,
                duration,
                estimated_cost
            FROM treatments
            WHERE id = ?
        """, (treatment_id,)).fetchone()

        if treatment is None:
            return None

        return dict(treatment)

    finally:

        connection.close()


# ============================================================
# DOCTOR FUNCTIONS
# ============================================================

def get_doctors():
    """
    Return all doctors along with their hospital name.
    """

    connection = get_connection()

    try:

        doctors = connection.execute("""
            SELECT
                doctors.id,
                doctors.name,
                doctors.specialty,
                doctors.hospital_id,
                doctors.city,
                doctors.experience,
                doctors.qualification,
                doctors.rating,
                doctors.description,
                hospitals.name AS hospital_name

            FROM doctors

            INNER JOIN hospitals
                ON doctors.hospital_id = hospitals.id

            ORDER BY doctors.name
        """).fetchall()

        return [dict(doctor) for doctor in doctors]

    finally:

        connection.close()


def get_doctor_by_id(doctor_id):
    """
    Return one doctor using its ID.
    """

    connection = get_connection()

    try:

        doctor = connection.execute("""
            SELECT
                doctors.id,
                doctors.name,
                doctors.specialty,
                doctors.hospital_id,
                doctors.city,
                doctors.experience,
                doctors.qualification,
                doctors.rating,
                doctors.description,
                hospitals.name AS hospital_name

            FROM doctors

            INNER JOIN hospitals
                ON doctors.hospital_id = hospitals.id

            WHERE doctors.id = ?
        """, (doctor_id,)).fetchone()

        if doctor is None:
            return None

        return dict(doctor)

    finally:

        connection.close()


# ============================================================
# PATIENT FUNCTIONS
# ============================================================

def get_patient_by_email(email):
    """
    Find an existing patient using their email.
    """

    connection = get_connection()

    try:

        patient = connection.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                country
            FROM patients
            WHERE LOWER(email) = LOWER(?)
        """, (email.strip(),)).fetchone()

        if patient is None:
            return None

        return dict(patient)

    finally:

        connection.close()


def create_patient(name, email, phone, country):
    """
    Create a new patient.

    If a patient with the same email already exists,
    return the existing patient's ID instead.
    """

    # -----------------------------
    # VALIDATION
    # -----------------------------

    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    country = country.strip()

    if not name:
        raise ValueError("Patient name is required.")

    if not email:
        raise ValueError("Patient email is required.")

    if "@" not in email:
        raise ValueError("Invalid email address.")

    if not phone:
        raise ValueError("Patient phone number is required.")

    if not country:
        raise ValueError("Patient country is required.")

    # -----------------------------
    # CHECK EXISTING PATIENT
    # -----------------------------

    existing_patient = get_patient_by_email(email)

    if existing_patient:

        return existing_patient["id"]

    # -----------------------------
    # CREATE NEW PATIENT
    # -----------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patients
            (
                name,
                email,
                phone,
                country
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            country
        ))

        patient_id = cursor.lastrowid

        connection.commit()

        return patient_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# APPOINTMENT VALIDATION
# ============================================================

def _validate_appointment_data(
    patient_id,
    hospital_id,
    treatment_id,
    doctor_id,
    appointment_date,
    appointment_time,
    consultation_type
):
    """
    Validate appointment-related IDs and values.
    """

    if not patient_id:
        raise ValueError("Invalid patient.")

    if not hospital_id:
        raise ValueError("Invalid hospital.")

    if not treatment_id:
        raise ValueError("Invalid treatment.")

    if not doctor_id:
        raise ValueError("Invalid doctor.")

    if not appointment_date:
        raise ValueError("Appointment date is required.")

    if not appointment_time:
        raise ValueError("Appointment time is required.")

    allowed_consultation_types = [
        "In-person Consultation",
        "Online Consultation"
    ]

    if consultation_type not in allowed_consultation_types:
        raise ValueError(
            "Invalid consultation type."
        )


# ============================================================
# CHECK APPOINTMENT SLOT
# ============================================================

def is_slot_available(
    doctor_id,
    appointment_date,
    appointment_time
):
    """
    Check whether a doctor is available at
    the selected date and time.
    """

    if not doctor_id:
        return False

    if not appointment_date:
        return False

    if not appointment_time:
        return False

    connection = get_connection()

    try:

        appointment = connection.execute("""
            SELECT id
            FROM appointments

            WHERE doctor_id = ?

            AND appointment_date = ?

            AND appointment_time = ?

            AND status != 'Rejected'
        """, (
            doctor_id,
            appointment_date,
            appointment_time
        )).fetchone()

        return appointment is None

    finally:

        connection.close()


# ============================================================
# CREATE APPOINTMENT
# ============================================================

def create_appointment(
    patient_id,
    hospital_id,
    treatment_id,
    doctor_id,
    appointment_date,
    appointment_time,
    consultation_type,
    message=""
):
    """
    Create and store a new appointment.
    """

    # -----------------------------
    # VALIDATE INPUT
    # -----------------------------

    _validate_appointment_data(
        patient_id,
        hospital_id,
        treatment_id,
        doctor_id,
        appointment_date,
        appointment_time,
        consultation_type
    )

    # -----------------------------
    # VERIFY PATIENT
    # -----------------------------

    patient = get_patient_by_id(patient_id)

    if patient is None:
        raise ValueError(
            "Patient does not exist."
        )

    # -----------------------------
    # VERIFY HOSPITAL
    # -----------------------------

    hospital = get_hospital_by_id(hospital_id)

    if hospital is None:
        raise ValueError(
            "Hospital does not exist."
        )

    # -----------------------------
    # VERIFY TREATMENT
    # -----------------------------

    treatment = get_treatment_by_id(treatment_id)

    if treatment is None:
        raise ValueError(
            "Treatment does not exist."
        )

    # -----------------------------
    # VERIFY DOCTOR
    # -----------------------------

    doctor = get_doctor_by_id(doctor_id)

    if doctor is None:
        raise ValueError(
            "Doctor does not exist."
        )

    # -----------------------------
    # VERIFY DOCTOR BELONGS
    # TO SELECTED HOSPITAL
    # -----------------------------

    if doctor["hospital_id"] != hospital_id:

        raise ValueError(
            "Selected doctor does not belong "
            "to the selected hospital."
        )

    # -----------------------------
    # CHECK SLOT
    # -----------------------------

    if not is_slot_available(
        doctor_id,
        appointment_date,
        appointment_time
    ):

        raise ValueError(
            "The selected appointment slot "
            "is already booked."
        )

    # -----------------------------
    # INSERT APPOINTMENT
    # -----------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO appointments
            (
                patient_id,
                hospital_id,
                treatment_id,
                doctor_id,
                appointment_date,
                appointment_time,
                consultation_type,
                message,
                status,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            hospital_id,
            treatment_id,
            doctor_id,
            appointment_date,
            appointment_time,
            consultation_type,
            message.strip(),
            "Pending",
            created_at
        ))

        appointment_id = cursor.lastrowid

        connection.commit()

        return appointment_id

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# PATIENT LOOKUP
# ============================================================

def get_patient_by_id(patient_id):
    """
    Return one patient using their ID.
    """

    connection = get_connection()

    try:

        patient = connection.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                country

            FROM patients

            WHERE id = ?
        """, (patient_id,)).fetchone()

        if patient is None:
            return None

        return dict(patient)

    finally:

        connection.close()


# ============================================================
# GET ALL APPOINTMENTS
# ============================================================

def get_appointments():
    """
    Return all appointments with related
    patient, hospital, treatment and doctor data.
    """

    connection = get_connection()

    try:

        appointments = connection.execute("""
            SELECT

                appointments.id,

                patients.name AS patient_name,
                patients.email,
                patients.phone,
                patients.country,

                hospitals.name AS hospital_name,

                treatments.name AS treatment_name,

                doctors.name AS doctor_name,

                appointments.appointment_date,
                appointments.appointment_time,

                appointments.consultation_type,

                appointments.message,

                appointments.status,

                appointments.created_at

            FROM appointments

            INNER JOIN patients
                ON appointments.patient_id = patients.id

            INNER JOIN hospitals
                ON appointments.hospital_id = hospitals.id

            INNER JOIN treatments
                ON appointments.treatment_id = treatments.id

            INNER JOIN doctors
                ON appointments.doctor_id = doctors.id

            ORDER BY appointments.created_at DESC

        """).fetchall()

        return [
            dict(appointment)
            for appointment in appointments
        ]

    finally:

        connection.close()


# ============================================================
# GET PATIENT APPOINTMENTS
# ============================================================

def get_patient_appointments(patient_id):
    """
    Return all appointments belonging to one patient.
    """

    if not patient_id:
        return []

    connection = get_connection()

    try:

        appointments = connection.execute("""
            SELECT

                appointments.id,

                hospitals.name AS hospital_name,

                treatments.name AS treatment_name,

                doctors.name AS doctor_name,

                appointments.appointment_date,

                appointments.appointment_time,

                appointments.consultation_type,

                appointments.message,

                appointments.status,

                appointments.created_at

            FROM appointments

            INNER JOIN hospitals
                ON appointments.hospital_id = hospitals.id

            INNER JOIN treatments
                ON appointments.treatment_id = treatments.id

            INNER JOIN doctors
                ON appointments.doctor_id = doctors.id

            WHERE appointments.patient_id = ?

            ORDER BY
                appointments.appointment_date,
                appointments.appointment_time

        """, (patient_id,)).fetchall()

        return [
            dict(appointment)
            for appointment in appointments
        ]

    finally:

        connection.close()


# ============================================================
# UPDATE APPOINTMENT STATUS
# ============================================================

def update_appointment_status(
    appointment_id,
    status
):
    """
    Update the status of an appointment.
    """

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Rejected"
    ]

    if status not in allowed_statuses:

        raise ValueError(
            "Invalid appointment status."
        )

    if not appointment_id:

        raise ValueError(
            "Invalid appointment ID."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE appointments

            SET status = ?

            WHERE id = ?
        """, (
            status,
            appointment_id
        ))

        if cursor.rowcount == 0:

            raise ValueError(
                "Appointment not found."
            )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# GET APPOINTMENT BY ID
# ============================================================

def get_appointment_by_id(appointment_id):
    """
    Return one complete appointment using its ID.
    """

    connection = get_connection()

    try:

        appointment = connection.execute("""
            SELECT

                appointments.id,

                patients.id AS patient_id,
                patients.name AS patient_name,
                patients.email,
                patients.phone,
                patients.country,

                hospitals.id AS hospital_id,
                hospitals.name AS hospital_name,

                treatments.id AS treatment_id,
                treatments.name AS treatment_name,

                doctors.id AS doctor_id,
                doctors.name AS doctor_name,

                appointments.appointment_date,
                appointments.appointment_time,
                appointments.consultation_type,
                appointments.message,
                appointments.status,
                appointments.created_at

            FROM appointments

            INNER JOIN patients
                ON appointments.patient_id = patients.id

            INNER JOIN hospitals
                ON appointments.hospital_id = hospitals.id

            INNER JOIN treatments
                ON appointments.treatment_id = treatments.id

            INNER JOIN doctors
                ON appointments.doctor_id = doctors.id

            WHERE appointments.id = ?

        """, (appointment_id,)).fetchone()

        if appointment is None:
            return None

        return dict(appointment)

    finally:

        connection.close()