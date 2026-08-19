
from database.database import get_connection


# ============================================================
# HOSPITAL DATA
# ============================================================

HOSPITALS = [
    {
        "name": "Apollo Hospital",
        "city": "Delhi",
        "specialty": "Cardiology",
        "rating": 4.8,
        "beds": 500,
        "description": (
            "A multi-specialty hospital providing advanced "
            "medical and cardiac care."
        ),
        "facilities": (
            "ICU, Emergency Care, Diagnostic Services, "
            "International Patient Services"
        )
    },
    {
        "name": "Fortis Hospital",
        "city": "Mumbai",
        "specialty": "Orthopedics",
        "rating": 4.7,
        "beds": 400,
        "description": (
            "A multi-specialty healthcare provider offering "
            "advanced orthopedic and surgical care."
        ),
        "facilities": (
            "ICU, Operation Theatres, Diagnostics, "
            "Physiotherapy"
        )
    },
    {
        "name": "Max Super Specialty Hospital",
        "city": "Chandigarh",
        "specialty": "Neurology",
        "rating": 4.6,
        "beds": 350,
        "description": (
            "A hospital providing specialized neurological "
            "and multi-specialty healthcare services."
        ),
        "facilities": (
            "Neurology Centre, ICU, Diagnostics, "
            "Emergency Services"
        )
    },
    {
        "name": "Medanta Hospital",
        "city": "Delhi",
        "specialty": "Oncology",
        "rating": 4.9,
        "beds": 600,
        "description": (
            "A multi-specialty healthcare institution with "
            "specialized cancer treatment services."
        ),
        "facilities": (
            "Cancer Centre, ICU, Diagnostics, "
            "International Patient Services"
        )
    },
    {
        "name": "Manipal Hospital",
        "city": "Bangalore",
        "specialty": "Cardiology",
        "rating": 4.7,
        "beds": 450,
        "description": (
            "A multi-specialty hospital offering advanced "
            "cardiac and medical services."
        ),
        "facilities": (
            "Cardiac Centre, ICU, Diagnostics, "
            "Emergency Services"
        )
    }
]


# ============================================================
# TREATMENT DATA
# ============================================================

TREATMENTS = [
    {
        "name": "Cardiac Surgery",
        "category": "Cardiology",
        "description": (
            "Surgical treatment for selected heart-related "
            "conditions."
        ),
        "duration": "2-4 weeks",
        "estimated_cost": 500000
    },
    {
        "name": "Knee Replacement",
        "category": "Orthopedics",
        "description": (
            "Surgical replacement of a damaged knee joint "
            "to improve mobility and reduce pain."
        ),
        "duration": "2-3 weeks",
        "estimated_cost": 250000
    },
    {
        "name": "Brain Tumor Treatment",
        "category": "Neurology",
        "description": (
            "Diagnosis and treatment planning for patients "
            "with brain tumors."
        ),
        "duration": "3-6 weeks",
        "estimated_cost": 450000
    },
    {
        "name": "Cancer Treatment",
        "category": "Oncology",
        "description": (
            "Cancer diagnosis, treatment planning and "
            "specialized oncology care."
        ),
        "duration": "4-8 weeks",
        "estimated_cost": 600000
    },
    {
        "name": "Angioplasty",
        "category": "Cardiology",
        "description": (
            "A procedure used to open narrowed or blocked "
            "blood vessels."
        ),
        "duration": "1-2 weeks",
        "estimated_cost": 200000
    },
    {
        "name": "Hip Replacement",
        "category": "Orthopedics",
        "description": (
            "Surgical replacement of a damaged hip joint "
            "to improve mobility."
        ),
        "duration": "2-4 weeks",
        "estimated_cost": 300000
    }
]


# ============================================================
# DOCTOR DATA
# ============================================================

DOCTORS = [
    {
        "name": "Dr. Raj Sharma",
        "specialty": "Cardiology",
        "hospital": "Apollo Hospital",
        "city": "Delhi",
        "experience": 15,
        "qualification": "MBBS, MD Cardiology",
        "rating": 4.9,
        "description": (
            "Cardiology specialist with experience in "
            "cardiac diagnosis and treatment."
        )
    },
    {
        "name": "Dr. Priya Kapoor",
        "specialty": "Orthopedics",
        "hospital": "Fortis Hospital",
        "city": "Mumbai",
        "experience": 12,
        "qualification": "MBBS, MS Orthopedics",
        "rating": 4.8,
        "description": (
            "Orthopedic specialist with experience in "
            "joint and bone-related treatments."
        )
    },
    {
        "name": "Dr. Aman Singh",
        "specialty": "Neurology",
        "hospital": "Max Super Specialty Hospital",
        "city": "Chandigarh",
        "experience": 10,
        "qualification": "MBBS, DM Neurology",
        "rating": 4.7,
        "description": (
            "Neurologist specializing in neurological "
            "disorders and related treatment."
        )
    },
    {
        "name": "Dr. Neha Verma",
        "specialty": "Oncology",
        "hospital": "Medanta Hospital",
        "city": "Delhi",
        "experience": 14,
        "qualification": "MBBS, MD Oncology",
        "rating": 4.9,
        "description": (
            "Oncology specialist providing cancer "
            "diagnosis and treatment."
        )
    },
    {
        "name": "Dr. Arjun Mehta",
        "specialty": "Cardiology",
        "hospital": "Manipal Hospital",
        "city": "Bangalore",
        "experience": 18,
        "qualification": "MBBS, DM Cardiology",
        "rating": 4.9,
        "description": (
            "Senior cardiologist specializing in "
            "advanced cardiac procedures."
        )
    }
]


# ============================================================
# INSERT HOSPITALS
# ============================================================

def insert_hospitals(connection):

    cursor = connection.cursor()

    for hospital in HOSPITALS:

        cursor.execute("""
            INSERT INTO hospitals
            (
                name,
                city,
                specialty,
                rating,
                beds,
                description,
                facilities
            )
            SELECT ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM hospitals
                WHERE name = ?
            )
        """, (
            hospital["name"],
            hospital["city"],
            hospital["specialty"],
            hospital["rating"],
            hospital["beds"],
            hospital["description"],
            hospital["facilities"],
            hospital["name"]
        ))


# ============================================================
# INSERT TREATMENTS
# ============================================================

def insert_treatments(connection):

    cursor = connection.cursor()

    for treatment in TREATMENTS:

        cursor.execute("""
            INSERT INTO treatments
            (
                name,
                category,
                description,
                duration,
                estimated_cost
            )
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM treatments
                WHERE name = ?
            )
        """, (
            treatment["name"],
            treatment["category"],
            treatment["description"],
            treatment["duration"],
            treatment["estimated_cost"],
            treatment["name"]
        ))


# ============================================================
# INSERT DOCTORS
# ============================================================

def insert_doctors(connection):

    cursor = connection.cursor()

    for doctor in DOCTORS:

        hospital = cursor.execute("""
            SELECT id
            FROM hospitals
            WHERE name = ?
        """, (
            doctor["hospital"],
        )).fetchone()

        if hospital is None:
            continue

        hospital_id = hospital[0]

        cursor.execute("""
            INSERT INTO doctors
            (
                name,
                specialty,
                hospital_id,
                city,
                experience,
                qualification,
                rating,
                description
            )
            SELECT ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM doctors
                WHERE name = ?
            )
        """, (
            doctor["name"],
            doctor["specialty"],
            hospital_id,
            doctor["city"],
            doctor["experience"],
            doctor["qualification"],
            doctor["rating"],
            doctor["description"],
            doctor["name"]
        ))


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def seed_database():

    connection = get_connection()

    try:

        insert_hospitals(connection)

        insert_treatments(connection)

        insert_doctors(connection)

        connection.commit()

        print("Healthcare data inserted successfully.")

    except Exception as error:

        connection.rollback()

        print(
            "Error while inserting healthcare data:"
        )

        print(error)

    finally:

        connection.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    seed_database()