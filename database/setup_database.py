import sqlite3

DATABASE_NAME = "medical_tourism.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # ==================================================
    # HOSPITALS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            specialty TEXT NOT NULL,
            rating REAL DEFAULT 0,
            beds INTEGER DEFAULT 0,
            description TEXT,
            facilities TEXT
        )
    """)

    # ==================================================
    # TREATMENTS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            duration TEXT,
            estimated_cost REAL DEFAULT 0
        )
    """)

    # ==================================================
    # DOCTORS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            hospital_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            experience INTEGER DEFAULT 0,
            qualification TEXT,
            rating REAL DEFAULT 0,
            description TEXT,

            FOREIGN KEY (hospital_id)
            REFERENCES hospitals(id)
        )
    """)

    # ==================================================
    # PATIENTS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    # ==================================================
    # APPOINTMENTS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,
            hospital_id INTEGER NOT NULL,
            treatment_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,

            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,

            consultation_type TEXT NOT NULL,

            message TEXT,

            status TEXT NOT NULL DEFAULT 'Pending',

            created_at TEXT NOT NULL,

            FOREIGN KEY (patient_id)
            REFERENCES patients(id),

            FOREIGN KEY (hospital_id)
            REFERENCES hospitals(id),

            FOREIGN KEY (treatment_id)
            REFERENCES treatments(id),

            FOREIGN KEY (doctor_id)
            REFERENCES doctors(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()
