
# HOSPITAL MANAGEMENT SYSTEM
# OPTION DISPLAY / MAIN MENU

import os
import shutil

from modules import session
from modules.patientregister import patient_registration
from modules.medicalhistory import medicalhistory
from modules.usercreation import user_doctor


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def option_display():

    user = session.get_user()

    if user is None:
        print("ERROR: No user is currently logged in.")
        return

    while True:

        clear_screen()

        width = shutil.get_terminal_size().columns
        width = max(width, 75)

        # HEADER

        print("HOSPITAL MANAGEMENT SYSTEM".center(width))
        print("HOSPITAL ADMINISTRATION PORTAL".center(width))

        # USER DETAILS

        print(f"Welcome, {user['name']}!".rjust(width - 2))
        print(f"Role: {user['role']}".rjust(width - 2))

        # MENU HEADING

        print("MAIN MENU".center(width))

        # PATIENT MANAGEMENT

        print("[PATIENT MANAGEMENT]")
        print("  1. Patient Registration")
        print("  2. Patient Details and Medical History")
        print("  3. Patient Upcoming Appointments")

        # STAFF MANAGEMENT

        print("[STAFF MANAGEMENT]")
        print("  4. User Creation (Doctor/Nurse/Admin/Manager)")
        print("  5. Doctor Management")
        print("  6. Staff Management")
        print("  7. Duty Management / Duty Scheduling")

        # FINANCE MANAGEMENT

        print("[FINANCE MANAGEMENT]")
        print("  8. Finance Manager Module")
        print("  9. Bill Generation and Billing Facilities")
        print("  10. Payment Verification and Receipt Generation")

        # REPORTS AND DOCUMENTS

        print("[REPORTS AND DOCUMENTS]")
        print("  11. Patient Report Creation for Doctors")
        print("  12. Patient Report Generation for Managers")
        print("  13. Prescription Generation (Dummy)")

        # ADMINISTRATION

        print("[ADMINISTRATION]")
        print("  14. Admin Profile Management")
        print("  15. Overall Reports and Statistics")

        # FOOTER

        print("  0. Exit")

        print("\nPlease select an option from the menu.")

        choice = menu_input()

        if choice == 0:
            print("Exiting the program. Goodbye!")
            session.clear_user()
            break

        menucalle(choice)

        input("\nPress Enter to return to the main menu...")


def menu_input():

    while True:

        try:
            choice = int(input("Enter your choice: "))

            if 0 <= choice <= 15:
                return choice

            else:
                print("Invalid choice! Please select between 0 and 15.")

        except ValueError:
            print("Please enter a valid number.")


def menucalle(inputid):

    # PATIENT MANAGEMENT

    if inputid == 1:
        patient_registration()

    elif inputid == 2:
        medicalhistory()

    elif inputid == 3:
        print("Patient Upcoming Appointments selected.")

    # STAFF MANAGEMENT

    elif inputid == 4:
        user_doctor()

    elif inputid == 5:
        print("Doctor Management selected.")

    elif inputid == 6:
        print("Staff Management selected.")

    elif inputid == 7:
        print("Duty Management / Duty Scheduling selected.")

    # FINANCE MANAGEMENT

    elif inputid == 8:
        print("Finance Manager Module selected.")

    elif inputid == 9:
        print("Bill Generation and Billing Facilities selected.")

    elif inputid == 10:
        print("Payment Verification and Receipt Generation selected.")

    # REPORTS AND DOCUMENTS

    elif inputid == 11:
        print("Patient Report Creation for Doctors selected.")

    elif inputid == 12:
        print("Patient Report Generation for Managers selected.")

    elif inputid == 13:
        print("Prescription Generation (Dummy) selected.")

    # ADMINISTRATION

    elif inputid == 14:
        print("Admin Profile Management selected.")

    elif inputid == 15:
        print("Overall Reports and Statistics selected.")
