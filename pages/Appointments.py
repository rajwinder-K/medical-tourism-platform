import streamlit as st
from datetime import date, time

from database.database import (
    get_hospitals,
    get_treatments,
    get_doctors,
    create_patient,
    create_appointment,
    is_slot_available
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Appointments",
    page_icon="📅",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📅 Book an Appointment")

st.write(
    "Request an appointment or consultation with a "
    "healthcare provider."
)

st.divider()


# ============================================================
# LOAD DATA FROM DATABASE
# ============================================================

try:

    hospitals = get_hospitals()
    treatments = get_treatments()
    doctors = get_doctors()

except Exception as error:

    st.error(
        "Unable to load appointment information."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# CHECK REQUIRED DATA
# ============================================================

if not hospitals:

    st.error(
        "No hospitals are available. "
        "Please contact the administrator."
    )

    st.stop()


if not treatments:

    st.error(
        "No treatments are available. "
        "Please contact the administrator."
    )

    st.stop()


if not doctors:

    st.error(
        "No doctors are available. "
        "Please contact the administrator."
    )

    st.stop()


# ============================================================
# PATIENT INFORMATION
# ============================================================

st.subheader("👤 Patient Information")

patient_name = st.text_input(
    "Full Name *",
    placeholder="Enter your full name"
)

col1, col2 = st.columns(2)

with col1:

    patient_email = st.text_input(
        "Email Address *",
        placeholder="example@email.com"
    )

with col2:

    patient_phone = st.text_input(
        "Phone Number *",
        placeholder="Enter your phone number"
    )


countries = [
    "India",
    "Canada",
    "United States",
    "United Kingdom",
    "Australia",
    "United Arab Emirates",
    "Other"
]

patient_country = st.selectbox(
    "Country *",
    countries
)


st.divider()


# ============================================================
# APPOINTMENT DETAILS
# ============================================================

st.subheader("🏥 Appointment Details")


# ------------------------------------------------------------
# HOSPITAL
# ------------------------------------------------------------

hospital_names = [
    hospital["name"]
    for hospital in hospitals
]

selected_hospital_name = st.selectbox(
    "Choose Hospital *",
    hospital_names
)


selected_hospital = next(
    (
        hospital
        for hospital in hospitals
        if hospital["name"] == selected_hospital_name
    ),
    None
)


# ------------------------------------------------------------
# TREATMENT
# ------------------------------------------------------------

treatment_names = [
    treatment["name"]
    for treatment in treatments
]

selected_treatment_name = st.selectbox(
    "Choose Treatment *",
    treatment_names
)


selected_treatment = next(
    (
        treatment
        for treatment in treatments
        if treatment["name"] == selected_treatment_name
    ),
    None
)


# ------------------------------------------------------------
# DOCTOR
# ------------------------------------------------------------

hospital_doctors = [
    doctor
    for doctor in doctors
    if doctor["hospital_name"] == selected_hospital_name
]


if not hospital_doctors:

    st.warning(
        "No doctors are currently available at this hospital."
    )

    st.stop()


doctor_options = [
    doctor["name"]
    for doctor in hospital_doctors
]


selected_doctor_name = st.selectbox(
    "Choose Doctor *",
    doctor_options
)


selected_doctor = next(
    (
        doctor
        for doctor in hospital_doctors
        if doctor["name"] == selected_doctor_name
    ),
    None
)


# ============================================================
# SELECTED PROVIDER INFORMATION
# ============================================================

if selected_doctor:

    with st.expander("👨‍⚕️ View Selected Doctor"):

        st.write(
            f"**Doctor:** {selected_doctor['name']}"
        )

        st.write(
            f"**Specialty:** {selected_doctor['specialty']}"
        )

        st.write(
            f"**Hospital:** {selected_doctor['hospital_name']}"
        )

        st.write(
            f"**Experience:** "
            f"{selected_doctor['experience']} years"
        )

        st.write(
            f"**Qualification:** "
            f"{selected_doctor['qualification']}"
        )

        st.write(
            f"⭐ **Rating:** {selected_doctor['rating']}"
        )


st.divider()


# ============================================================
# CONSULTATION TYPE
# ============================================================

st.subheader("💻 Consultation Type")

consultation_type = st.radio(
    "Choose consultation type *",
    [
        "In-person Consultation",
        "Online Consultation"
    ],
    horizontal=True
)


# ============================================================
# DATE AND TIME
# ============================================================

st.subheader("📅 Choose Date and Time")

col1, col2 = st.columns(2)


with col1:

    appointment_date = st.date_input(
        "Appointment Date *",
        min_value=date.today()
    )


with col2:

    appointment_time = st.time_input(
        "Appointment Time *",
        value=time(10, 0)
    )


# ============================================================
# ADDITIONAL MESSAGE
# ============================================================

message = st.text_area(
    "Additional Information",
    placeholder=(
        "Describe your medical requirement or "
        "any additional information for the provider."
    ),
    height=120
)


st.divider()


# ============================================================
# SUBMIT APPOINTMENT
# ============================================================

st.subheader("📨 Submit Appointment Request")

st.write(
    "Please review your information before submitting "
    "your appointment request."
)


submit_appointment = st.button(
    "📅 Request Appointment",
    type="primary",
    use_container_width=True
)


# ============================================================
# VALIDATION AND SUBMISSION
# ============================================================

if submit_appointment:

    # --------------------------------------------------------
    # PATIENT VALIDATION
    # --------------------------------------------------------

    if not patient_name.strip():

        st.error(
            "Please enter your full name."
        )

        st.stop()


    if not patient_email.strip():

        st.error(
            "Please enter your email address."
        )

        st.stop()


    if "@" not in patient_email:

        st.error(
            "Please enter a valid email address."
        )

        st.stop()


    if not patient_phone.strip():

        st.error(
            "Please enter your phone number."
        )

        st.stop()


    # --------------------------------------------------------
    # DATE VALIDATION
    # --------------------------------------------------------

    if appointment_date < date.today():

        st.error(
            "Please select today or a future date."
        )

        st.stop()


    # --------------------------------------------------------
    # DOCTOR VALIDATION
    # --------------------------------------------------------

    if selected_doctor is None:

        st.error(
            "Please select a doctor."
        )

        st.stop()


    # --------------------------------------------------------
    # CHECK DOCTOR SLOT
    # --------------------------------------------------------

    try:

        available = is_slot_available(
            selected_doctor["id"],
            appointment_date.isoformat(),
            appointment_time.strftime("%H:%M")
        )

    except Exception as error:

        st.error(
            "Unable to check appointment availability."
        )

        st.caption(
            f"Database error: {error}"
        )

        st.stop()


    if not available:

        st.error(
            "This doctor is already booked for the "
            "selected date and time."
        )

        st.info(
            "Please choose another time."
        )

        st.stop()


    # --------------------------------------------------------
    # CREATE PATIENT AND APPOINTMENT
    # --------------------------------------------------------

    try:

        patient_id = create_patient(
            name=patient_name.strip(),
            email=patient_email.strip(),
            phone=patient_phone.strip(),
            country=patient_country
        )


        appointment_id = create_appointment(
            patient_id=patient_id,
            hospital_id=selected_hospital["id"],
            treatment_id=selected_treatment["id"],
            doctor_id=selected_doctor["id"],
            appointment_date=appointment_date.isoformat(),
            appointment_time=appointment_time.strftime("%H:%M"),
            consultation_type=consultation_type,
            message=message.strip()
        )


    except Exception as error:

        st.error(
            "Unable to submit your appointment request."
        )

        st.caption(
            f"Database error: {error}"
        )

        st.stop()


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    st.success(
        "✅ Appointment request submitted successfully!"
    )

    st.info(
        f"Your appointment request ID is: "
        f"APT-{appointment_id:04d}"
    )

    st.write(
        "**Status:** Pending"
    )

    st.write(
        "The appointment request has been saved and "
        "will be reviewed by the administration."
  )
