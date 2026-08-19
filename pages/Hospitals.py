import streamlit as st

from database.database import get_hospitals


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hospitals",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🏥 Find Hospitals")

st.write(
    "Explore healthcare providers and find hospitals "
    "that match your requirements."
)

st.divider()


# ============================================================
# LOAD HOSPITAL DATA FROM DATABASE
# ============================================================

try:
    hospitals = get_hospitals()

except Exception as error:

    st.error(
        "Unable to load hospital information."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# CHECK DATABASE
# ============================================================

if not hospitals:

    st.warning(
        "No hospital information is currently available."
    )

    st.stop()


# ============================================================
# FILTER OPTIONS
# ============================================================

hospital_names = ["All Hospitals"] + sorted(
    {
        hospital["name"]
        for hospital in hospitals
    }
)

cities = ["All Cities"] + sorted(
    {
        hospital["city"]
        for hospital in hospitals
    }
)

specialties = ["All Specialties"] + sorted(
    {
        hospital["specialty"]
        for hospital in hospitals
    }
)


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader("🔎 Choose Your Requirements")

col1, col2, col3 = st.columns(3)


with col1:

    selected_hospital = st.selectbox(
        "🏥 Choose Hospital",
        hospital_names
    )


with col2:

    selected_city = st.selectbox(
        "📍 Choose City",
        cities
    )


with col3:

    selected_specialty = st.selectbox(
        "🩺 Choose Specialty",
        specialties
    )


# Rating filter

rating_options = [
    0,
    1,
    2,
    3,
    4,
    4.5,
    4.7,
    4.8,
    4.9
]

minimum_rating = st.select_slider(
    "⭐ Minimum Rating",
    options=rating_options,
    value=0
)


st.divider()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_hospitals = hospitals


if selected_hospital != "All Hospitals":

    filtered_hospitals = [
        hospital
        for hospital in filtered_hospitals
        if hospital["name"] == selected_hospital
    ]


if selected_city != "All Cities":

    filtered_hospitals = [
        hospital
        for hospital in filtered_hospitals
        if hospital["city"] == selected_city
    ]


if selected_specialty != "All Specialties":

    filtered_hospitals = [
        hospital
        for hospital in filtered_hospitals
        if hospital["specialty"] == selected_specialty
    ]


if minimum_rating > 0:

    filtered_hospitals = [
        hospital
        for hospital in filtered_hospitals
        if hospital["rating"] >= minimum_rating
    ]


# ============================================================
# RESULTS
# ============================================================

st.subheader(
    f"🏥 Available Hospitals ({len(filtered_hospitals)})"
)


if not filtered_hospitals:

    st.warning(
        "No hospitals match your selected requirements."
    )

    st.stop()


# ============================================================
# HOSPITAL CARDS
# ============================================================

for hospital in filtered_hospitals:

    with st.container(border=True):

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        col1, col2 = st.columns([4, 1])


        with col1:

            st.subheader(
                hospital["name"]
            )

            st.write(
                f"📍 **City:** {hospital['city']}"
            )

            st.write(
                f"🩺 **Specialty:** {hospital['specialty']}"
            )

            st.write(
                f"🛏️ **Beds:** {hospital['beds']}"
            )


        with col2:

            st.metric(
                "⭐ Rating",
                hospital["rating"]
            )


        # ----------------------------------------------------
        # HOSPITAL DETAILS
        # ----------------------------------------------------

        with st.expander("View Hospital Details"):

            st.write(
                f"### {hospital['name']}"
            )

            st.write(
                f"**Location:** {hospital['city']}"
            )

            st.write(
                f"**Specialty:** {hospital['specialty']}"
            )

            st.write(
                f"**Available Beds:** {hospital['beds']}"
            )

            st.write(
                f"**Rating:** ⭐ {hospital['rating']}"
            )

            st.write(
                f"**About:** {hospital['description']}"
            )

            st.write(
                f"**Facilities:** {hospital['facilities']}"
            )
