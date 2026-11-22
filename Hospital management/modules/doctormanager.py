
import os
import shutil

from modules import session

from database.doctordatabasemanagement import (
    get_doctor_profile,
    get_dashboard_counts,
    get_assigned_patients,
    get_patient_for_doctor,
    get_all_doctors,
    save_consultation,
    get_patient_consultations
)


# =========================================================
# GENERAL FUNCTIONS
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_width():
    return max(shutil.get_terminal_size().columns, 75)


def get_input(label):
    return input(f"{label:<25}: ").strip()


def pause():
    input("\nPress Enter to continue...")


def display_header(user, width):

    print("=" * width)
    print("DOCTOR MANAGEMENT DASHBOARD".center(width))
    print("=" * width)

    print(f"Welcome, {user['name']}".rjust(width))
    print(f"Role: {user['role']}".rjust(width))

    print("=" * width)


# =========================================================
# PATIENT DISPLAY
# =========================================================

def display_patient(patient):

    print("\n" + "-" * 55)

    print(f"Patient ID       : {patient['patient_id']}")
    print(f"Patient Code     : {patient.get('patient_code')}")
    print(f"Patient Name     : {patient['patient_name']}")
    print(f"Age              : {patient['age']}")
    print(f"Gender           : {patient['gender']}")
    print(f"Patient Type     : {patient['patient_type']}")

    if patient.get("blood_group"):
        print(f"Blood Group      : {patient['blood_group']}")

    if patient.get("doctor_name"):
        print(f"Assigned Doctor  : {patient['doctor_name']}")

    print("-" * 55)


# =========================================================
# DOCTOR SELECTION
# =========================================================

def select_doctor():
    
    doctors = get_all_doctors()

    if doctors is None:
        print("\nUnable to retrieve doctor records.")
        return None

    if not doctors:
        print("\nNo doctors found.")
        return None

    print("\nAVAILABLE DOCTORS")
    print("=" * 75)

    for doctor in doctors:

        print(
            f"\n{doctor['doctor_id']}. "
            f"{doctor['name']} | "
            f"{doctor['department']} | "
            f"{doctor['specialization'] or 'General'}"
        )

    print("\n" + "=" * 75)

    try:
        doctor_id = int(input("Enter Doctor ID: ").strip())
    except ValueError:
        print("\nInvalid Doctor ID.")
        return None

    selected = next(
        (d for d in doctors if d["doctor_id"] == doctor_id),
        None
    )

    if selected is None:
        print("\nDoctor not found.")
        return None

    return selected


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard(doctor=None, user_role="doctor"):

    clear_screen()

    width = get_width()

    if user_role == "doctor":
        doctor_id = doctor["doctor_id"]
        title = "DOCTOR DASHBOARD"
    else:
        doctor_id = None
        title = "HOSPITAL-WIDE DOCTOR STATISTICS"

    counts = get_dashboard_counts(doctor_id)

    print(title.center(width))
    print("=" * width)

    if counts is None:
        print("\nUnable to load dashboard statistics.")
        pause()
        return

    if doctor:
        print(f"\nDoctor Name      : {doctor['name']}")
        print(f"Department       : {doctor['department']}")
        print(f"Specialization   : {doctor['specialization'] or 'Not specified'}")

    print("\n" + "=" * width)
    print("STATISTICS".center(width))
    print("=" * width)

    print(f"\nTotal Assigned Patients : {counts['total_patients']}")
    print(f"Total Consultations     : {counts['total_consultations']}")

    pause()


# =========================================================
# VIEW PATIENTS
# =========================================================

def show_assigned_patients(doctor_id=None):

    clear_screen()

    print("PATIENT RECORDS".center(get_width()))
    print("=" * get_width())

    patients = get_assigned_patients(doctor_id)

    if patients is None:
        print("\nUnable to retrieve patients.")

    elif not patients:
        print("\nNo patient records found.")

    else:
        for patient in patients:
            display_patient(patient)

    pause()


# =========================================================
# SEARCH PATIENTS
# =========================================================

def search_patient(doctor_id=None):

    clear_screen()

    print("SEARCH PATIENT RECORDS".center(get_width()))
    print("=" * get_width())

    search_value = get_input("Patient name or code")

    if not search_value:
        print("\nSearch value cannot be empty.")
        pause()
        return

    patients = get_patient_for_doctor(
        doctor_id,
        search_value
    )

    if patients is None:
        print("\nUnable to search patients.")

    elif not patients:
        print("\nNo matching patients found.")

    else:
        for patient in patients:
            display_patient(patient)

    pause()


# =========================================================
# CREATE CONSULTATION
# =========================================================

def create_consultation(doctor=None, user_role="doctor"):

    clear_screen()

    print("CREATE PATIENT CONSULTATION".center(get_width()))
    print("=" * get_width())

    # Doctors use their own doctor profile.
    # Admins and Managers select the responsible doctor.

    if user_role == "doctor":

        selected_doctor = doctor

    else:

        selected_doctor = select_doctor()

        if selected_doctor is None:
            pause()
            return

    try:
        patient_id = int(get_input("Patient ID"))
    except ValueError:
        print("\nPlease enter a valid numeric Patient ID.")
        pause()
        return

    # Verify patient access.
    patient_list = get_patient_for_doctor(
        selected_doctor["doctor_id"],
        str(patient_id)
    )

    if patient_list is None:
        print("\nUnable to verify patient access.")
        pause()
        return

    patient = next(
        (
            p for p in patient_list
            if p["patient_id"] == patient_id
        ),
        None
    )

    if patient is None:
        print("\nPatient is not actively assigned to this doctor.")
        pause()
        return

    display_patient(patient)

    print("\nRESPONSIBLE DOCTOR")
    print("-" * 55)

    print(f"Doctor Name : {selected_doctor['name']}")
    print(f"Department  : {selected_doctor['department']}")

    print("\nENTER CONSULTATION DETAILS")
    print("-" * 55)

    symptoms = get_input("Symptoms")
    observations = get_input("Observations")
    diagnosis = get_input("Diagnosis")

    if not diagnosis:
        print("\nDiagnosis cannot be empty.")
        pause()
        return

    treatment_plan = get_input("Treatment Plan")
    notes = get_input("Additional Notes")

    confirm = input(
        "\nSave this consultation? (Y/N): "
    ).strip().lower()

    if confirm != "y":
        print("\nConsultation cancelled.")
        pause()
        return

    result = save_consultation(
        selected_doctor["doctor_id"],
        patient_id,
        symptoms,
        observations,
        diagnosis,
        treatment_plan,
        notes
    )

    if result:
        print("\nConsultation saved successfully!")
        print(f"Responsible Doctor: {selected_doctor['name']}")
    else:
        print("\nUnable to save consultation.")

    pause()


# =========================================================
# CONSULTATION HISTORY
# =========================================================

def view_consultation_history(doctor_id=None):

    clear_screen()

    print("PATIENT CONSULTATION HISTORY".center(get_width()))
    print("=" * get_width())

    try:
        patient_id = int(get_input("Patient ID"))
    except ValueError:
        print("\nPlease enter a valid numeric Patient ID.")
        pause()
        return

    # Verify patient access.
    patient_list = get_patient_for_doctor(
        doctor_id,
        str(patient_id)
    )

    if patient_list is None:
        print("\nUnable to verify patient access.")
        pause()
        return

    patient = next(
        (
            p for p in patient_list
            if p["patient_id"] == patient_id
        ),
        None
    )

    if patient is None:
        print("\nPatient not found or access denied.")
        pause()
        return

    display_patient(patient)

    records = get_patient_consultations(
        doctor_id,
        patient_id
    )

    if records is None:
        print("\nUnable to retrieve consultation history.")

    elif not records:
        print("\nNo previous consultations found.")

    else:

        for record in records:

            print("\n" + "-" * 65)

            print(f"Consultation ID : {record['consultation_id']}")
            print(f"Doctor          : {record.get('doctor_name', 'Unknown')}")
            print(f"Department      : {record.get('department', 'Unknown')}")
            print(f"Date            : {record['consultation_date']}")
            print(f"Symptoms        : {record['symptoms']}")
            print(f"Observations    : {record['observations']}")
            print(f"Diagnosis       : {record['diagnosis']}")
            print(f"Treatment Plan  : {record['treatment_plan']}")
            print(f"Notes           : {record['notes']}")

        print("\n" + "-" * 65)

    pause()


# =========================================================
# MAIN DOCTOR MANAGEMENT MODULE
# =========================================================

def doctor_module():

    user = session.get_user()

    if user is None:
        print("No active user session!")
        pause()
        return

    allowed_roles = {
        "doctor",
        "admin",
        "manager"
    }

    user_role = user.get("role", "").strip().lower()

    if user_role not in allowed_roles:

        print("ACCESS DENIED!")
        print(
            "Only Doctors, Admins, and Managers "
            "can access this module."
        )

        pause()
        return

    # Fetch doctor profile only for doctors.
    doctor = None

    if user_role == "doctor":

        doctor = get_doctor_profile(
            user["user_id"]
        )

        if doctor is None:
            print("Doctor profile not found.")
            print("Please contact the administrator.")
            pause()
            return

    while True:

        clear_screen()

        width = get_width()

        display_header(user, width)

        if user_role == "doctor":
            print("\n1. Doctor Dashboard")
            print("2. View My Assigned Patients")
            print("3. Search My Patients")
            print("4. Create Patient Consultation")
            print("5. View My Consultation History")

        else:
            print("\n1. Hospital-Wide Dashboard")
            print("2. View All Patients")
            print("3. Search All Patients")
            print("4. Create Consultation")
            print("5. View All Consultation History")

        print("\n0. Return to Main Menu")

        print("\n" + "=" * width)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_dashboard(doctor, user_role)

        elif choice == "2":
            doctor_id = (
                doctor["doctor_id"]
                if user_role == "doctor"
                else None
            )

            show_assigned_patients(doctor_id)

        elif choice == "3":
            doctor_id = (
                doctor["doctor_id"]
                if user_role == "doctor"
                else None
            )

            search_patient(doctor_id)

        elif choice == "4":
            create_consultation(doctor, user_role)

        elif choice == "5":
            doctor_id = (
                doctor["doctor_id"]
                if user_role == "doctor"
                else None
            )

            view_consultation_history(doctor_id)

        elif choice == "0":
            break

        else:
            print("\nInvalid choice!")
            pause()
