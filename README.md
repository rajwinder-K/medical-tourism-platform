# medical-tourism-platform
Medical tourism platform MVP for international patients


## Individual Contribution
```
Rajwinder Kaur - setup_database.py, app.py, ai recommendation 
Jeenam - Hospitals.py, Doctors.py
Husan - database.py, sample_data.py
kamal - admin.py
jashan - Treatments.py
Lovepreet - appointments.py
```

# MediTour — Medical Tourism Platform

MediTour is a medical tourism platform that helps patients discover, compare and select suitable hospitals, treatments and doctors in one place.

# Problem

Medical-tourism information is often scattered across different sources. Patients may find it difficult to compare hospitals, doctors, treatments, costs, ratings and available options before making a decision.

# Solution

MediTour provides a single platform for:

-  Hospital discovery and filtering
-  Treatment discovery and filtering
-  Doctor discovery and filtering
-  AI-assisted healthcare recommendations
-  Appointment/consultation requests
-  Admin management

Patient Journey

Discover → Filter → Recommend → Compare → Select → Book

# AI Recommendation

The recommendation system uses patient preferences such as city, specialty, budget and rating to identify and rank suitable healthcare options.

The current MVP uses an explainable preference-based scoring system, not a trained ML model.

Example:

Delhi + Cardiology + Budget ₹5 lakh + Rating ≥ 4.5

The system ranks the healthcare options that best match these requirements.

# Technology Stack

- Python
- Streamlit
- SQLite
- Preference-based Recommendation

# Main Files

- "app.py" — Home page and main navigation
- "Hospitals.py" — Hospital filtering
- "Treatments.py" — Treatment filtering
- "Doctors.py" — Doctor filtering
- "Appointments.py" — Appointment requests
- "Admin.py" — Admin management
- "database.py" — Database connection and operations
- "setup_database.py" — Creates database tables
- "sample_data.py" — Inserts healthcare data
- "recommendation.py" — Recommendation logic

# How to Run
```
1. Download the Project

From GitHub:

Code → Download ZIP

Extract the ZIP and open the project folder in VS Code.

2. Install Requirements

Open the terminal inside the project folder:

pip install -r requirements.txt

3. Create Database

python database/setup_database.py

4. Insert Data

python data/sample_data.py

5. Run the Application

streamlit run app.py

The application will open in the browser.
```

# Important Order
```
Always run:

setup_database.py
       ↓
sample_data.py
       ↓
streamlit run app.py
```

# Team Collaboration

The project is maintained through the GitHub website.

Team members:

1. Create/edit their assigned files in VS Code.
2. Test their changes locally.
3. Upload the files directly to the correct GitHub folder.
4. Commit the changes on GitHub.

All members should maintain the same project structure and coordinate before modifying the same file.

# Future Scope

- Real hospital/provider APIs
- Real-time doctor and appointment availability
- Patient authentication
- Online consultation
- Notifications
- Multilingual support
- Travel and accommodation assistance
- Cloud deployment
- ML-based personalized recommendation

# Project Goal

MediTour aims to make medical tourism simpler, more personalized and more organized by connecting healthcare discovery, recommendation and appointment management in one platform.

Discover → Filter → Recommend → Compare → Book → Manage
