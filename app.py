import streamlit as st
from ai.recommendation import get_recommendations


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MediTour",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏥 MediTour")
    st.caption("Medical Tourism Platform")

    st.divider()

    st.markdown("### 🧭 Navigation")

    # CLICKABLE NAVIGATION
    st.page_link(
        "app.py",
        label="Home",
        icon="🏠"
    )

    st.page_link(
        "pages/Hospitals.py",
        label="Hospitals",
        icon="🏥"
    )

    st.page_link(
        "pages/Treatments.py",
        label="Treatments",
        icon="🩺"
    )

    st.page_link(
        "pages/Doctors.py",
        label="Doctors",
        icon="👨‍⚕️"
    )

    st.page_link(
        "pages/Appointments.py",
        label="Appointments",
        icon="📅"
    )

    st.page_link(
        "pages/Admin.py",
        label="Admin",
        icon="⚙️"
    )

    st.divider()

    st.markdown("### 💡 Quick Guide")

    st.write(
        "Explore hospitals, treatments and doctors, "
        "then request an appointment."
    )

    st.divider()

    st.caption("MediTour • Healthcare Platform")


# ============================================================
# HOME PAGE
# ============================================================

st.title("🏥 Welcome to MediTour")

st.subheader(
    "Your healthcare journey starts here."
)

st.write(
    """
    Medical Tour is a medical tourism platform that helps
    patients discover hospitals, explore treatments,
    find suitable doctors and request medical
    consultations in one place.
    """
)
st.divider()
# ============================================================
# FEATURE SECTION
# ============================================================

st.header("✨ Explore Medical Tour")


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("🏥 Hospitals")

    st.write(
        "Explore hospitals by city, specialty, "
        "rating and available facilities."
    )

    st.page_link(
        "pages/Hospitals.py",
        label="Explore Hospitals →",
        icon="🏥"
    )


with col2:

    st.subheader("🩺 Treatments")

    st.write(
        "Explore available treatments with "
        "categories, duration and estimated cost."
    )

    st.page_link(
        "pages/Treatments.py",
        label="Explore Treatments →",
        icon="🩺"
    )


with col3:

    st.subheader("👨‍⚕️ Doctors")

    st.write(
        "Find doctors according to specialty, "
        "hospital, experience and rating."
    )

    st.page_link(
        "pages/Doctors.py",
        label="Find Doctors →",
        icon="👨‍⚕️"
    )


st.divider()


# ============================================================
# HOW IT WORKS
# ============================================================

st.header("🚀 How It Works")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("### 1️⃣ Explore")

    st.write(
        "Browse hospitals, treatments and doctors."
    )


with col2:

    st.markdown("### 2️⃣ Choose")

    st.write(
        "Select the healthcare option you prefer."
    )


with col3:

    st.markdown("### 3️⃣ Request")

    st.write(
        "Submit an appointment or consultation request."
    )


with col4:

    st.markdown("### 4️⃣ Manage")

    st.write(
        "Your appointment request is stored and managed."
    )


st.divider()

# ============================================================
# AI RECOMMENDATION SYSTEM
# ============================================================

st.divider()

st.header("🤖 AI-Powered Recommendations")

st.write(
    """
    Tell us your preferences and MediTour will recommend
    suitable hospitals, treatments and doctors.
    """
)


# ------------------------------------------------------------
# GET RECOMMENDATION DATA
# ------------------------------------------------------------

try:

    hospitals_data = get_recommendations(
        limit=100
    )

except Exception:

    st.error(
        "Unable to load recommendation data."
    )

    st.stop()


# ------------------------------------------------------------
# GET CITIES AND SPECIALTIES FROM DATABASE
# ------------------------------------------------------------

cities = sorted(set(
    item["data"].get("city")
    for item in hospitals_data.get("hospitals", [])
    if item["data"].get("city")
))

specialties = sorted(set(
    item["data"].get("specialty")
    for item in hospitals_data.get("hospitals", [])
    if item["data"].get("specialty")
))


# ------------------------------------------------------------
# USER PREFERENCES
# ------------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    city = st.selectbox(
        "📍 Preferred City",
        ["All"] + cities
    )


with col2:

    specialty = st.selectbox(
        "🩺 Medical Specialty",
        ["All"] + specialties
    )


col1, col2 = st.columns(2)


with col1:

    budget = st.number_input(
        "💰 Maximum Treatment Budget",
        min_value=0,
        value=0,
        step=1000
    )


with col2:

    minimum_rating = st.slider(
        "⭐ Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )


# ------------------------------------------------------------
# GET RECOMMENDATIONS
# ------------------------------------------------------------

if st.button(
    "🤖 Get My Recommendations",
    type="primary",
    use_container_width=True
):

    maximum_budget = None

    if budget > 0:
        maximum_budget = budget


    recommendations = get_recommendations(

        city=city,

        specialty=specialty,

        treatment_category="All",

        maximum_budget=maximum_budget,

        minimum_rating=minimum_rating,

        limit=5
    )


    # ========================================================
    # RECOMMENDED HOSPITALS
    # ========================================================

    st.subheader("🏥 Recommended Hospitals")

    hospitals = recommendations.get(
        "hospitals",
        []
    )


    if hospitals:

        for index, item in enumerate(hospitals):

            hospital = item.get(
                "data",
                {}
            )

            with st.container(border=True):

                st.markdown(
                    f"### 🏥 {hospital.get('name', 'Hospital')}"
                )

                st.write(
                    f"📍 **City:** "
                    f"{hospital.get('city', 'N/A')}"
                )

                st.write(
                    f"🩺 **Specialty:** "
                    f"{hospital.get('specialty', 'N/A')}"
                )

                st.write(
                    f"⭐ **Rating:** "
                    f"{hospital.get('rating', 'N/A')}"
                )


    else:

        st.info(
            "No hospitals match your preferences."
        )


    # ========================================================
    # RECOMMENDED TREATMENTS
    # ========================================================

    st.subheader("🩺 Recommended Treatments")

    treatments = recommendations.get(
        "treatments",
        []
    )


    if treatments:

        for index, item in enumerate(treatments):

            treatment = item.get(
                "data",
                {}
            )

            with st.container(border=True):

                st.markdown(
                    f"### 🩺 "
                    f"{treatment.get('name', 'Treatment')}"
                )

                st.write(
                    f"📂 **Category:** "
                    f"{treatment.get('category', 'N/A')}"
                )

                st.write(
                    f"💰 **Estimated Cost:** "
                    f"{treatment.get('estimated_cost', 'N/A')}"
                )


    else:

        st.info(
            "No treatments match your preferences."
        )


    # ========================================================
    # RECOMMENDED DOCTORS
    # ========================================================

    st.subheader("👨‍⚕️ Recommended Doctors")

    doctors = recommendations.get(
        "doctors",
        []
    )


    if doctors:

        for index, item in enumerate(doctors):

            doctor = item.get(
                "data",
                {}
            )

            with st.container(border=True):

                st.markdown(
                    f"### 👨‍⚕️ "
                    f"{doctor.get('name', 'Doctor')}"
                )

                st.write(
                    f"🩺 **Specialty:** "
                    f"{doctor.get('specialty', 'N/A')}"
                )

                st.write(
                    f"🏥 **Hospital:** "
                    f"{doctor.get('hospital_name', 'N/A')}"
                )

                st.write(
                    f"💼 **Experience:** "
                    f"{doctor.get('experience', 'N/A')} years"
                )

                st.write(
                    f"⭐ **Rating:** "
                    f"{doctor.get('rating', 'N/A')}"
                )


    else:

        st.info(
            "No doctors match your preferences."
        )

st.divider()

# ============================================================
# APPOINTMENT SECTION
# ============================================================

st.header("📅 Book a Consultation")

st.write(
    """
    Select a hospital, treatment and doctor,
    choose your preferred consultation type,
    date and time, and submit your appointment request.
    """
)

st.page_link(
    "pages/Appointments.py",
    label="Request an Appointment",
    icon="📅"
)


st.divider()

# ============================================================
# ADMIN SECTION
# ============================================================

st.header("⚙️ Administration")

st.write(
    """
    Appointment requests can be reviewed and their
    status can be managed from the administration dashboard.
    """
)

st.page_link(
    "pages/Admin.py",
    label="Open Admin Dashboard",
    icon="⚙️"
)

st.divider()

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "🏥 MediTour | Medical Tourism Platform | "
    "Explore • Choose • Connect"
)
