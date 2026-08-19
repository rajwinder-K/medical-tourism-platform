import streamlit as st

from database.database import get_treatments


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Treatments",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🩺 Explore Treatments")

st.write(
    "Explore available medical treatments, their categories, "
    "duration, and estimated cost."
)

st.divider()


# ============================================================
# LOAD TREATMENT DATA FROM DATABASE
# ============================================================

try:

    treatments = get_treatments()

except Exception as error:

    st.error(
        "Unable to load treatment information."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# CHECK DATABASE
# ============================================================

if not treatments:

    st.warning(
        "No treatment information is currently available."
    )

    st.stop()


# ============================================================
# FILTER OPTIONS
# ============================================================

treatment_names = ["All Treatments"] + sorted(
    {
        treatment["name"]
        for treatment in treatments
    }
)

categories = ["All Categories"] + sorted(
    {
        treatment["category"]
        for treatment in treatments
    }
)


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader("🔎 Choose Your Requirements")

col1, col2 = st.columns(2)


with col1:

    selected_treatment = st.selectbox(
        "🩺 Choose Treatment",
        treatment_names
    )


with col2:

    selected_category = st.selectbox(
        "📂 Choose Category",
        categories
    )


st.divider()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_treatments = treatments


if selected_treatment != "All Treatments":

    filtered_treatments = [
        treatment
        for treatment in filtered_treatments
        if treatment["name"] == selected_treatment
    ]


if selected_category != "All Categories":

    filtered_treatments = [
        treatment
        for treatment in filtered_treatments
        if treatment["category"] == selected_category
    ]


# ============================================================
# RESULTS
# ============================================================

st.subheader(
    f"🩺 Available Treatments ({len(filtered_treatments)})"
)


if not filtered_treatments:

    st.warning(
        "No treatments match your selected requirements."
    )

    st.stop()


# ============================================================
# TREATMENT CARDS
# ============================================================

for treatment in filtered_treatments:

    with st.container(border=True):

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        st.subheader(
            treatment["name"]
        )

        st.write(
            f"📂 **Category:** {treatment['category']}"
        )

        st.write(
            f"⏱️ **Estimated Duration:** {treatment['duration']}"
        )

        st.write(
            f"💰 **Estimated Cost:** ₹{treatment['estimated_cost']:,.0f}"
        )


        # ----------------------------------------------------
        # TREATMENT DETAILS
        # ----------------------------------------------------

        with st.expander("View Treatment Details"):

            st.write(
                f"### {treatment['name']}"
            )

            st.write(
                f"**Category:** {treatment['category']}"
            )

            st.write(
                f"**Description:** {treatment['description']}"
            )

            st.write(
                f"**Estimated Duration:** "
                f"{treatment['duration']}"
            )

            st.write(
                f"**Estimated Cost:** "
                f"₹{treatment['estimated_cost']:,.0f}"
)
