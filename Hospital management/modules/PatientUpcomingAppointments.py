
# PATIENT DETAILS AND MEDICAL HISTORY

import os
import shutil

from modules import session
from database.dbconnector import get_connector


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_width():
    return max(shutil.get_terminal_size().columns, 75)


def display_header(user, width):

    print("\n" + "HOSPITAL MANAGEMENT SYSTEM".center(width))
    print("HOSPITAL ADMINISTRATION PORTAL".center(width))

    print(f"\nWelcome, {user['name']}!".rjust(width))
    print(f"Role: {user['role']}".rjust(width))

    print("\n" + "=" * 45)
    print("PATIENT DETAILS AND MEDICAL HISTORY".center(width))
    print("=" * 45)


def display_patient(patient):

    print("\n" + "=" * 55)
    print("PATIENT INFORMATION")
    print("=" * 55)

    details = {
        "Patient ID": patient.get("patient_id"),
        "Patient Code": patient.get("patient_code"),
        "Patient Name": patient.get("patient_name"),
        "Date of Birth": patient.get("dob"),
        "Age": patient.get("age"),
        "Gender": patient.get("gender"),
        "Profession": patient.get("profession"),
        "Monthly Income": patient.get("income"),
        "Blood Group": patient.get("blood_group"),
        "Patient Type": patient.get("patient_type"),
        "Registration Date": patient.get("registration_date")
    }

    print("\n--- PERSONAL DETAILS ---")

    for key, value in details.items():
        print(f"{key:<22}: {value if value is not None else 'N/A'}")

    print("\n--- CONTACT DETAILS ---")

    contacts = {
        "Address": patient.get("address"),
        "Mobile Number": patient.get("mobile_number"),
        "Secondary Number": patient.get("secondary_number"),
        "Email": patient.get("email"),
        "Emergency Contact": patient.get("emergency_contact")
    }

    for key, value in contacts.items():
        print(f"{key:<22}: {value if value else 'N/A'}")

    print("\n--- IDENTIFICATION DETAILS ---")

    print(f"{'ID Proof Type':<22}: {patient.get('id_proof_type') or 'N/A'}")
    print(f"{'ID Proof Number':<22}: {patient.get('id_proof_number') or 'N/A'}")

    print("=" * 55)


def fetch_patients(query=None, params=()):

    connection = get_connector()

    if connection is None:
        print("\nDatabase connection failed!")
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query or """
            SELECT *
            FROM patient_registration
            ORDER BY patient_id ASC
        """, params)

        patients = cursor.fetchall()

        for patient in patients:
            patient["patient_code"] = f"P{patient['patient_id']:04d}"

        return patients

    except Exception as error:
        print(f"\nUnable to retrieve patients: {error}")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_all_patients():
    return fetch_patients()


def get_patient_by_name(name):

    return fetch_patients("""
        SELECT *
        FROM patient_registration
        WHERE patient_name LIKE %s
        ORDER BY patient_name ASC
    """, (f"%{name}%",))


def get_patient_by_id(patient_id):

    patient_id = str(patient_id).strip().upper()

    if patient_id.startswith("P"):
        patient_id = patient_id[1:]

    if not patient_id.isdigit():
        return []

    return fetch_patients("""
        SELECT *
        FROM patient_registration
        WHERE patient_id = %s
    """, (int(patient_id),))


def medicalhistory():

    user = session.get_user()

    if user is None:
        print("\nNo active user session!")
        input("\nPress Enter to continue...")
        return

    width = get_width()

    while True:

        clear_screen()
        display_header(user, width)

        print("\n1. Show All Patients")
        print("2. Search Patient by Name")
        print("3. Search Patient by ID / Code")
        print("0. Return to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            clear_screen()
            display_header(user, width)

            patients = get_all_patients()

            if patients is None:
                print("\nUnable to load patient records.")

            elif patients:
                print(f"\nTotal Patients: {len(patients)}")

                for patient in patients:
                    display_patient(patient)

            else:
                print("\nNo patients registered.")

            input("\nPress Enter to continue...")

        elif choice == "2":

            name = input("\nEnter Patient Name: ").strip()

            if not name:
                print("\nPatient name cannot be empty.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_name(name)

            if patients is None:
                print("\nUnable to search patient records.")

            elif patients:
                print(f"\nMatching Patients: {len(patients)}")

                for patient in patients:
                    display_patient(patient)

            else:
                print("\nNo matching patient found.")

            input("\nPress Enter to continue...")

        elif choice == "3":

            patient_id = input(
                "\nEnter Patient ID or Code (e.g. 1 or P0001): "
            ).strip()

            if not patient_id:
                print("\nPatient ID cannot be empty.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_id(patient_id)

            if patients is None:
                print("\nUnable to search patient records.")

            elif patients:
                display_patient(patients[0])

            else:
                print("\nNo patient found with that ID or code.")

            input("\nPress Enter to continue...")

        elif choice == "0":
            break

        else:
            print("\nInvalid choice!")
            input("\nPress Enter to continue...")
