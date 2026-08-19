import streamlit as st

from database.database import (
    get_appointments,
    update_appointment_status
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("⚙️ Admin Dashboard")

st.write(
    "Manage and monitor appointment requests submitted "
    "through the medical tourism platform."
)

st.divider()


# ============================================================
# LOAD APPOINTMENTS
# ============================================================

try:

    appointments = get_appointments()

except Exception as error:

    st.error(
        "Unable to load appointment information."
    )

    st.caption(
        f"Database error: {error}"
    )

    st.stop()


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

total_appointments = len(appointments)

pending_appointments = sum(
    appointment["status"] == "Pending"
    for appointment in appointments
)

confirmed_appointments = sum(
    appointment["status"] == "Confirmed"
    for appointment in appointments
)

rejected_appointments = sum(
    appointment["status"] == "Rejected"
    for appointment in appointments
)


st.subheader("📊 Appointment Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total",
        total_appointments
    )


with col2:

    st.metric(
        "Pending",
        pending_appointments
    )


with col3:

    st.metric(
        "Confirmed",
        confirmed_appointments
    )


with col4:

    st.metric(
        "Rejected",
        rejected_appointments
    )


st.divider()


# ============================================================
# CHECK APPOINTMENTS
# ============================================================

st.subheader("📋 Appointment Requests")


if not appointments:

    st.info(
        "There are currently no appointment requests."
    )

    st.stop()


# ============================================================
# FILTER BY STATUS
# ============================================================

status_options = [
    "All",
    "Pending",
    "Confirmed",
    "Rejected"
]


selected_status = st.selectbox(
    "Filter by Status",
    status_options
)


if selected_status == "All":

    filtered_appointments = appointments

else:

    filtered_appointments = [
        appointment
        for appointment in appointments
        if appointment["status"] == selected_status
    ]


st.write(
    f"Showing {len(filtered_appointments)} appointment(s)"
)


st.divider()


# ============================================================
# APPOINTMENT DETAILS
# ============================================================

for appointment in filtered_appointments:

    with st.container(border=True):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        col1, col2 = st.columns([4, 1])


        with col1:

            st.subheader(
                f"Appointment #{appointment['id']}"
            )

            st.write(
                f"👤 **Patient:** "
                f"{appointment['patient_name']}"
            )

            st.write(
                f"🏥 **Hospital:** "
                f"{appointment['hospital_name']}"
            )

            st.write(
                f"🩺 **Treatment:** "
                f"{appointment['treatment_name']}"
            )

            st.write(
                f"👨‍⚕️ **Doctor:** "
                f"{appointment['doctor_name']}"
            )


        with col2:

            status = appointment["status"]


            if status == "Pending":

                st.warning(
                    "⏳ Pending"
                )

            elif status == "Confirmed":

                st.success(
                    "✅ Confirmed"
                )

            else:

                st.error(
                    "❌ Rejected"
                )


        # ----------------------------------------------------
        # APPOINTMENT INFORMATION
        # ----------------------------------------------------

        with st.expander("View Complete Details"):

            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Patient Name:** "
                    f"{appointment['patient_name']}"
                )

                st.write(
                    f"**Email:** "
                    f"{appointment['email']}"
                )

                st.write(
                    f"**Phone:** "
                    f"{appointment['phone']}"
                )

                st.write(
                    f"**Country:** "
                    f"{appointment['country']}"
                )


            with col2:

                st.write(
                    f"**Date:** "
                    f"{appointment['appointment_date']}"
                )

                st.write(
                    f"**Time:** "
                    f"{appointment['appointment_time']}"
                )

                st.write(
                    f"**Consultation:** "
                    f"{appointment['consultation_type']}"
                )

                st.write(
                    f"**Current Status:** "
                    f"{appointment['status']}"
                )


            if appointment["message"]:

                st.write(
                    "**Patient Message:**"
                )

                st.info(
                    appointment["message"]
                )


        # ----------------------------------------------------
        # STATUS MANAGEMENT
        # ----------------------------------------------------

        if appointment["status"] == "Pending":

            st.write(
                "**Update Appointment:**"
            )

            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "✅ Confirm Appointment",
                    key=f"confirm_{appointment['id']}",
                    use_container_width=True
                ):

                    try:

                        update_appointment_status(
                            appointment["id"],
                            "Confirmed"
                        )

                        st.success(
                            "Appointment confirmed."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            "Unable to confirm appointment."
                        )

                        st.caption(
                            f"Database error: {error}"
                        )


            with col2:

                if st.button(
                    "❌ Reject Appointment",
                    key=f"reject_{appointment['id']}",
                    use_container_width=True
                ):

                    try:

                        update_appointment_status(
                            appointment["id"],
                            "Rejected"
                        )

                        st.success(
                            "Appointment rejected."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            "Unable to reject appointment."
                        )

                        st.caption(
                            f"Database error: {error}"
                        )


        elif appointment["status"] == "Confirmed":

            if st.button(
                "↩️ Mark as Pending",
                key=f"pending_{appointment['id']}"
            ):

                try:

                    update_appointment_status(
                        appointment["id"],
                        "Pending"
                    )

                    st.success(
                        "Appointment moved back to pending."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Unable to update appointment."
                    )

                    st.caption(
                        f"Database error: {error}"
                    )


        elif appointment["status"] == "Rejected":

            if st.button(
                "↩️ Restore to Pending",
                key=f"restore_{appointment['id']}"
            ):

                try:

                    update_appointment_status(
                        appointment["id"],
                        "Pending"
                    )

                    st.success(
                        "Appointment restored to pending."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Unable to update appointment."
                    )

                    st.caption(
                        f"Database error: {error}"
                    )
