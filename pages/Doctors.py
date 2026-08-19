import streamlit as st

from database.database import get_doctors


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Doctors",
    page_icon="👨‍⚕️",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("👨‍⚕️ Find Doctors")

st.write(
    "Explore healthcare providers by specialty, hospital, "
    "location, experience, and rating."
)

st.divider()


# ============================================================
# LOAD DOCTOR DATA FROM DATABASE
# ============================================================

try:

    doctors = get_doctors()

except Exception as error:

    st.error(
        "Unable to load doctor information."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# CHECK DATABASE
# ============================================================

if not doctors:

    st.warning(
        "No doctor information is currently available."
    )

    st.stop()


# ============================================================
# FILTER OPTIONS
# ============================================================

doctor_names = ["All Doctors"] + sorted(
    {
        doctor["name"]
        for doctor in doctors
    }
)

specialties = ["All Specialties"] + sorted(
    {
        doctor["specialty"]
        for doctor in doctors
    }
)

hospital_names = ["All Hospitals"] + sorted(
    {
        doctor["hospital_name"]
        for doctor in doctors
    }
)

cities = ["All Cities"] + sorted(
    {
        doctor["city"]
        for doctor in doctors
    }
)


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader("🔎 Choose Your Requirements")

col1, col2 = st.columns(2)


with col1:

    selected_doctor = st.selectbox(
        "👨‍⚕️ Choose Doctor",
        doctor_names
    )


with col2:

    selected_specialty = st.selectbox(
        "🩺 Choose Specialty",
        specialties
    )


col3, col4 = st.columns(2)


with col3:

    selected_hospital = st.selectbox(
        "🏥 Choose Hospital",
        hospital_names
    )


with col4:

    selected_city = st.selectbox(
        "📍 Choose City",
        cities
    )


# ============================================================
# EXPERIENCE FILTER
# ============================================================

experience_options = sorted(
    {
        doctor["experience"]
        for doctor in doctors
    }
)

if experience_options:

    minimum_experience = st.select_slider(
        "💼 Minimum Experience (Years)",
        options=[0] + experience_options,
        value=0
    )

else:

    minimum_experience = 0


# ============================================================
# RATING FILTER
# ============================================================

rating_options = sorted(
    {
        doctor["rating"]
        for doctor in doctors
    }
)

if rating_options:

    minimum_rating = st.select_slider(
        "⭐ Minimum Rating",
        options=[0] + rating_options,
        value=0
    )

else:

    minimum_rating = 0


st.divider()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_doctors = doctors


if selected_doctor != "All Doctors":

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["name"] == selected_doctor
    ]


if selected_specialty != "All Specialties":

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["specialty"] == selected_specialty
    ]


if selected_hospital != "All Hospitals":

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["hospital_name"] == selected_hospital
    ]


if selected_city != "All Cities":

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["city"] == selected_city
    ]


if minimum_experience > 0:

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["experience"] >= minimum_experience
    ]


if minimum_rating > 0:

    filtered_doctors = [
        doctor
        for doctor in filtered_doctors
        if doctor["rating"] >= minimum_rating
    ]


# ============================================================
# RESULTS
# ============================================================

st.subheader(
    f"👨‍⚕️ Available Doctors ({len(filtered_doctors)})"
)


if not filtered_doctors:

    st.warning(
        "No doctors match your selected requirements."
    )

    st.stop()


# ============================================================
# DOCTOR CARDS
# ============================================================

for doctor in filtered_doctors:

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])


        # ----------------------------------------------------
        # DOCTOR INFORMATION
        # ----------------------------------------------------

        with col1:

            st.subheader(
                f"👨‍⚕️ {doctor['name']}"
            )

            st.write(
                f"🩺 **Specialty:** {doctor['specialty']}"
            )

            st.write(
                f"🏥 **Hospital:** {doctor['hospital_name']}"
            )

            st.write(
                f"📍 **City:** {doctor['city']}"
            )

            st.write(
                f"💼 **Experience:** "
                f"{doctor['experience']} years"
            )


        # ----------------------------------------------------
        # RATING
        # ----------------------------------------------------

        with col2:

            st.metric(
                "⭐ Rating",
                doctor["rating"]
            )


        # ----------------------------------------------------
        # DOCTOR DETAILS
        # ----------------------------------------------------

        with st.expander("View Doctor Details"):

            st.write(
                f"### 👨‍⚕️ {doctor['name']}"
            )

            st.write(
                f"**Specialty:** {doctor['specialty']}"
            )

            st.write(
                f"**Hospital:** {doctor['hospital_name']}"
            )

            st.write(
                f"**City:** {doctor['city']}"
            )

            st.write(
                f"**Experience:** "
                f"{doctor['experience']} years"
            )

            st.write(
                f"**Qualification:** "
                f"{doctor['qualification']}"
            )

            st.write(
                f"**Rating:** ⭐ {doctor['rating']}"
            )

            st.write(
                f"**About:** {doctor['description']}"
            )
