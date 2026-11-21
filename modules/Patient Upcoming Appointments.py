
# PATIENT UPCOMING APPOINTMENTS


# PATIENT DETAILS AND MEDICAL HISTORY

import os
import shutil

from modules import session
from database.dbconnector import get_connector


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header(user, width):

    print("HOSPITAL MANAGEMENT SYSTEM".center(width))
    print("HOSPITAL ADMINISTRATION PORTAL".center(width))

    # USER DETAILS - RIGHT CORNER

    print(f"Welcome, {user['name']}!".rjust(width))
    print(f"Role: {user['role']}".rjust(width))

    print()
    print(("=" * 40).center(width))
    print("PATIENT DETAILS AND MEDICAL HISTORY".center(width))
    print(("=" * 40).center(width))


def display_patient(patient):

    print("\n" + "=" * 45)
    print("PATIENT INFORMATION")
    print("=" * 45)

    print(f"Patient ID          : {patient['patient_id']}")
    print(f"Patient Code        : {patient['patient_code']}")
    print(f"Patient Name        : {patient['patient_name']}")
    print(f"Date of Birth       : {patient['dob']}")
    print(f"Age                 : {patient['age']}")
    print(f"Gender              : {patient['gender']}")
    print(f"Profession          : {patient['profession']}")
    print(f"Monthly Income      : {patient['income']}")

    print("\n--- CONTACT DETAILS ---")

    print(f"Address             : {patient['address']}")
    print(f"Mobile Number       : {patient['mobile_number']}")
    print(f"Secondary Number    : {patient['secondary_number']}")
    print(f"Email               : {patient['email']}")
    print(f"Emergency Contact   : {patient['emergency_contact']}")

    print("\n--- IDENTIFICATION DETAILS ---")

    print(f"ID Proof            : {patient['id_proof']}")
    print(f"ID Proof Number     : {patient['id_proof_number']}")

    print("\n--- MEDICAL DETAILS ---")

    print(f"Blood Group         : {patient['blood_group']}")
    print(f"Patient Type        : {patient['patient_type']}")
    print(f"Registration Date   : {patient['registration_date']}")

    print("=" * 45)


def get_all_patients():

    connection = get_connector()

    if connection is None:
        print("\nDatabase connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM patients
            ORDER BY patient_id ASC
        """)

        return cursor.fetchall()

    except Exception as error:

        print("\nUnable to retrieve patients:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


def get_patient_by_name(name):

    connection = get_connector()

    if connection is None:
        print("\nDatabase connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE patient_name LIKE %s
            ORDER BY patient_name ASC
        """, (f"%{name}%",))

        return cursor.fetchall()

    except Exception as error:

        print("\nUnable to search patients:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


def get_patient_by_id(patient_id):

    connection = get_connector()

    if connection is None:
        print("\nDatabase connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE patient_id = %s
               OR patient_code = %s
        """, (patient_id, patient_id))

        return cursor.fetchall()

    except Exception as error:

        print("\nUnable to search patient:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


def medicalhistory():

    user = session.get_user()

    if user is None:
        print("No active user session!")
        input("\nPress Enter to continue...")
        return

    width = max(shutil.get_terminal_size().columns, 75)

    while True:

        clear_screen()

        display_header(user, width)

        print("\n1. Show All Patients")
        print("2. Show Patient by Name")
        print("3. Show Patient by ID")
        print("0. Return to Main Menu")

        try:
            choice = int(input("\nEnter your choice: "))

        except ValueError:
            print("\nPlease enter a valid number.")
            input("\nPress Enter to continue...")
            continue

        # SHOW ALL PATIENTS

        if choice == 1:

            clear_screen()
            display_header(user, width)

            patients = get_all_patients()

            if patients is not None:

                if patients:

                    print(f"\nTotal Patients: {len(patients)}")

                    for patient in patients:
                        display_patient(patient)

                else:
                    print("\nNo patients registered.")

            input("\nPress Enter to continue...")

        # SEARCH BY NAME

        elif choice == 2:

            name = input("\nEnter Patient Name: ").strip()

            if not name:
                print("\nPlease enter a patient name.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_name(name)

            if patients is not None:

                if patients:

                    print(f"\nMatching Patients: {len(patients)}")

                    for patient in patients:
                        display_patient(patient)

                else:
                    print("\nNo matching patient found.")

            input("\nPress Enter to continue...")

        # SEARCH BY ID

        elif choice == 3:

            patient_id = input(
                "\nEnter Patient ID or Patient Code: "
            ).strip()

            if not patient_id:
                print("\nPlease enter a Patient ID or Code.")
                input("\nPress Enter to continue...")
                continue

            clear_screen()
            display_header(user, width)

            patients = get_patient_by_id(patient_id)

            if patients is not None:

                if patients:
                    display_patient(patients[0])

                else:
                    print("\nNo patient found with that ID.")

            input("\nPress Enter to continue...")

        # RETURN TO MENU

        elif choice == 0:

            break

        else:

            print("\nInvalid choice!")
            input("\nPress Enter to continue...")
