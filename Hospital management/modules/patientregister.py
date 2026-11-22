
# PATIENT REGISTER

import os
import shutil
from modules import session
from datetime import datetime
from database.dbutility import save_patient


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# ALIGNED INPUT FUNCTION

def get_input(label, length=35):
    return input(f"{label.ljust(length)}: ")



def patient_registration():

    user = session.get_user()

    if user is None:
        print("No active user session!")
        input("\nPress Enter to continue...")
        return

    clear_screen()

    width = max(shutil.get_terminal_size().columns, 75)

    # HEADER

    print("HOSPITAL MANAGEMENT SYSTEM".center(width))
    print("HOSPITAL ADMINISTRATION PORTAL".center(width))

    print(f"Welcome, {user['name']}!".rjust(width))
    print(f"Role: {user['role']}".rjust(width))

    print()
    print(("=" * 30).center(width))
    print("PATIENT REGISTRATION".center(width))
    print(("=" * 30).center(width))

    # PERSONAL DETAILS

    print("\n--- PERSONAL DETAILS ---")

    patient_name = get_input("Enter Patient Name").strip()
    dob_input = get_input("Enter Date of Birth (DD-MM-YYYY)").strip()
    # DATE VALIDATION
    
    try:
        dob = datetime.strptime(dob_input, "%d-%m-%Y").date()
    except ValueError:
        print("\nInvalid date! Use DD-MM-YYYY.")
        dob = get_input("Enter Date of Birth (DD-MM-YYYY)").strip()
        return
    age_input = get_input("Enter Age").strip()
    if int(age_input) >0 and int(age_input) < 99:
        age = int(age_input)
    else:
        print("\nInvalid age!")
        input("\nPress Enter to continue...")
        return
    gender = get_input("Enter Gender").strip()
    profession = get_input("Enter Profession").strip()
    income_input = get_input("Enter Monthly Income (Optional)").strip()

    # CONTACT DETAILS

    print("\n--- CONTACT DETAILS ---")

    address = get_input("Enter Address").strip()
    mobile_number = get_input("Enter Mobile Number").strip()
    secondary_number = get_input("Enter Secondary Number (Optional)").strip()
    email = get_input("Enter Email Address (Optional)").strip()
    emergency_contact = get_input("Enter Emergency Contact Number").strip()

    # IDENTIFICATION DETAILS

    print("\n--- IDENTIFICATION DETAILS ---")

    id_proof = get_input("Enter ID Proof Type").strip()
    id_proof_number = get_input("Enter ID Proof Reference Number").strip()

    # MEDICAL DETAILS

    print("\n--- BASIC MEDICAL DETAILS ---")

    blood_group = get_input("Enter Blood Group").strip()

    print("\nPatient Type:")
    print("1. Inpatient")
    print("2. Outpatient")

    patient_type_input = get_input("Select Patient Type").strip()

    if patient_type_input == "1":
        patient_type = "Inpatient"

    elif patient_type_input == "2":
        patient_type = "Outpatient"

    else:
        print("\nInvalid Patient Type!")
        input("\nPress Enter to continue...")
        return

    # REQUIRED FIELD VALIDATION

    required_fields = [
        patient_name,
        gender,
        profession,
        address,
        mobile_number,
        emergency_contact,
        id_proof,
        id_proof_number
    ]

    if not all(required_fields):
        print("\nPlease fill in all required fields!")
        input("\nPress Enter to continue...")
        return

# PREPARE PATIENT DATA

    patient_data = (
        patient_name,
        dob,
        age,
        gender,
        profession,
        income_input,
        address,
        mobile_number,
        secondary_number or None,
        email or None,
        emergency_contact,
        id_proof,
        id_proof_number,
        blood_group or None,
        patient_type
    )

    # SAVE TO DATABASE

    result = save_patient(patient_data)

    if result:

        patient_id, patient_code = result

        print("\nPATIENT REGISTRATION SUCCESSFUL!")

        print(f"Patient ID   : {patient_id}")
        print(f"Patient Code : {patient_code}")
        print(f"Patient Name : {patient_name}")

    else:

        print("\nPATIENT REGISTRATION FAILED!")

    input("\nPress Enter to return to the main menu...")


