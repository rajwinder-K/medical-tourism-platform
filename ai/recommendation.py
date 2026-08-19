from database.database import (
    get_hospitals,
    get_treatments,
    get_doctors
)


def recommend_hospitals(city="All", specialty="All",
                        minimum_rating=0, limit=5):

    hospitals = get_hospitals()
    results = []

    for hospital in hospitals:

        hospital_city = str(hospital.get("city", ""))
        hospital_specialty = str(hospital.get("specialty", ""))

        try:
            rating = float(hospital.get("rating", 0))
        except:
            rating = 0

        # Filter city
        if city != "All":
            if hospital_city.lower() != city.lower():
                continue

        # Filter specialty
        if specialty != "All":
            if hospital_specialty.lower() != specialty.lower():
                continue

        # Filter rating
        if rating < minimum_rating:
            continue

        # Recommendation score
        score = rating * 20

        if city != "All":
            score += 30

        if specialty != "All":
            score += 30

        results.append({
            "data": hospital,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:limit]


def recommend_treatments(category="All",
                          maximum_budget=None,
                          limit=5):

    treatments = get_treatments()
    results = []

    for treatment in treatments:

        treatment_category = str(
            treatment.get("category", "")
        )

        try:
            cost = float(
                treatment.get("estimated_cost", 0)
            )
        except:
            cost = 0

        # Category filter
        if category != "All":

            if treatment_category.lower() != category.lower():
                continue

        # Budget filter
        if maximum_budget is not None:

            if cost > maximum_budget:
                continue

        score = 50

        # Give cheaper treatments a higher score
        if maximum_budget is not None and maximum_budget > 0:

            score += (
                (maximum_budget - cost)
                / maximum_budget
            ) * 50

        results.append({
            "data": treatment,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:limit]


def recommend_doctors(specialty="All",
                      hospital="All",
                      minimum_experience=0,
                      minimum_rating=0,
                      limit=5):

    doctors = get_doctors()
    results = []

    for doctor in doctors:

        doctor_specialty = str(
            doctor.get("specialty", "")
        )

        doctor_hospital = str(
            doctor.get("hospital_name", "")
        )

        try:
            experience = float(
                doctor.get("experience", 0)
            )
        except:
            experience = 0

        try:
            rating = float(
                doctor.get("rating", 0)
            )
        except:
            rating = 0

        # Specialty filter
        if specialty != "All":

            if doctor_specialty.lower() != specialty.lower():
                continue

        # Hospital filter
        if hospital != "All":

            if doctor_hospital.lower() != hospital.lower():
                continue

        # Experience filter
        if experience < minimum_experience:
            continue

        # Rating filter
        if rating < minimum_rating:
            continue

        # Recommendation score
        score = (
            rating * 10
            + experience * 2
        )

        if specialty != "All":
            score += 30

        if hospital != "All":
            score += 20

        results.append({
            "data": doctor,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:limit]


def get_recommendations(
    city="All",
    specialty="All",
    hospital="All",
    treatment_category="All",
    maximum_budget=None,
    minimum_experience=0,
    minimum_rating=0,
    limit=5
):

    return {
        "hospitals": recommend_hospitals(
            city=city,
            specialty=specialty,
            minimum_rating=minimum_rating,
            limit=limit
        ),

        "treatments": recommend_treatments(
            category=treatment_category,
            maximum_budget=maximum_budget,
            limit=limit
        ),

        "doctors": recommend_doctors(
            specialty=specialty,
            hospital=hospital,
            minimum_experience=minimum_experience,
            minimum_rating=minimum_rating,
            limit=limit
        )
    }
