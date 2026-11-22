
# ==========================================
# PATIENT DETAILS AND MEDICAL HISTORY
# ==========================================

import os
import shutil

from modules import session

from database.dbutility import (
    get_all_patients,
    get_patient_by_name,
    get_patient_by_id
)


# ==========================================
# CLEAR SCREEN
# ==========================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# ==========================================
# HEADER
# ==========================================

def display_header(user, width):

    print("HOSPITAL MANAGEMENT SYSTEM".center(width))
    print("HOSPITAL ADMINISTRATION PORTAL".center(width))

    print(f"Welcome, {user['name']}!".rjust(width))
    print(f"Role: {user['role']}".rjust(width))

    print()
    print(("=" * 30).center(width))
    print("PATIENT REGISTRATION".center(width))
    print(("=" * 30).center(width))


# ==========================================
# DISPLAY PATIENT DETAILS
# ==========================================

def display_patient(patient):

    print("\n" + "=" * 55)
    print("PATIENT INFORMATION")
    print("=" * 55)

    print(f"Patient ID          : {patient.get('patient_id', 'N/A')}")
    print(f"Patient Code        : {patient.get('patient_code', 'N/A')}")
    print(f"Patient Name        : {patient.get('patient_name', 'N/A')}")
    print(f"Date of Birth       : {patient.get('dob', 'N/A')}")
    print(f"Age                 : {patient.get('age', 'N/A')}")
    print(f"Gender              : {patient.get('gender', 'N/A')}")
    print(f"Profession          : {patient.get('profession', 'N/A')}")
    print(f"Monthly Income      : {patient.get('income', 'N/A')}")

    print("\n--- CONTACT DETAILS ---")

    print(f"Address             : {patient.get('address', 'N/A')}")
    print(f"Mobile Number       : {patient.get('mobile_number', 'N/A')}")
    print(f"Secondary Number    : {patient.get('secondary_number') or 'N/A'}")
    print(f"Email               : {patient.get('email') or 'N/A'}")
    print(f"Emergency Contact   : {patient.get('emergency_contact') or 'N/A'}")

    print("\n--- IDENTIFICATION DETAILS ---")

    print(f"ID Proof            : {patient.get('id_proof', 'N/A')}")
    print(f"ID Proof Number     : {patient.get('id_proof_number', 'N/A')}")

    print("\n--- MEDICAL DETAILS ---")

    print(f"Blood Group         : {patient.get('blood_group') or 'N/A'}")
    print(f"Patient Type        : {patient.get('patient_type', 'N/A')}")
    print(f"Registration Date   : {patient.get('registration_date', 'N/A')}")

    print("=" * 55)


# ==========================================
# DISPLAY PATIENT RECORDS
# ==========================================

def display_patients(patients):

    if patients is None:
        print("\nUnable to retrieve patient records.")
        return

    if not patients:
        print("\nNo matching patient records found.")
        return

    print(f"\nTotal Patients Found: {len(patients)}")

    for patient in patients:
        display_patient(patient)


# ==========================================
# PATIENT MEDICAL HISTORY MODULE
# ==========================================

def medicalhistory():

    user = session.get_user()

    if user is None:
        print("No active user session!")
        input("\nPress Enter to continue...")
        return

    # ======================================
    # INITIAL SCREEN HEADER
    # ======================================
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

    # ======================================
    # MAIN MENU
    # ======================================

    while True:

        clear_screen()

        display_header(user, width)

        print("\n1. Show All Patients")
        print("2. Show Patient by Name")
        print("3. Show Patient by ID or Code")
        print("0. Return to Main Menu")

        print("\n" + "=" * 55)

        try:
            choice = int(input("\nEnter your choice: "))

        except ValueError:
            print("\nPlease enter a valid number.")
            input("\nPress Enter to continue...")
            continue


        # ==================================
        # SHOW ALL PATIENTS
        # ==================================

        if choice == 1:

            clear_screen()
            display_header(user, width)

            patients = get_all_patients()

            display_patients(patients)

            input("\nPress Enter to continue...")


        # ==================================
        # SEARCH PATIENT BY NAME
        # ==================================

        elif choice == 2:

            name = input("\nEnter Patient Name: ").strip()

            if not name:
                print("\nPlease enter a patient name.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_name(name)

            display_patients(patients)

            input("\nPress Enter to continue...")


        # ==================================
        # SEARCH PATIENT BY ID OR CODE
        # ==================================

        elif choice == 3:

            patient_identifier = input(
                "\nEnter Patient ID or Patient Code: "
            ).strip()

            if not patient_identifier:
                print("\nPlease enter a Patient ID or Patient Code.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_id(patient_identifier)

            display_patients(patients)

            input("\nPress Enter to continue...")


        # ==================================
        # RETURN TO MAIN MENU
        # ==================================

        elif choice == 0:

            break


        else:

            print("\nInvalid choice!")
            input("\nPress Enter to continue...")
