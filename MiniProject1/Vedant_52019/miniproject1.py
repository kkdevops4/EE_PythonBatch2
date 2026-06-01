def get_priority(age, symptom):

    symptom = symptom.lower()

    if symptom == "emergency":
        return 1

    elif age >= 60:
        return 2

    elif symptom == "fever":
        return 3

    else:
        return 4


patients = []

num_patients = int(input("Enter number of patients: "))

for i in range(num_patients):

    print("\nEnter details for Patient", i + 1)

    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    symptom = input("Enter patient symptom: ")

    priority = get_priority(age, symptom)

    patient = {
        "name": name,
        "age": age,
        "symptom": symptom,
        "priority": priority
    }

    patients.append(patient)


patients.sort(key=lambda patient: patient["priority"])


print("\n===== PATIENT QUEUE =====")

for patient in patients:

    print(
        patient["name"],
        "| Age:", patient["age"],
        "| Symptom:", patient["symptom"],
        "| Priority:", patient["priority"]
    )


doctors = ["Dr. Sharma", "Dr. Patel"]

print("\n || DOCTOR ASSIGNMENTS ||")

for i in range(len(patients)):

    doctor = doctors[i % len(doctors)]

    print(patients[i]["name"], "is assigned to", doctor)