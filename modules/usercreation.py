
# USER CREATION MODULE

import os
import shutil
from modules import session


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(label, length=35):
    return input(f"{label.ljust(length)}: ")


def user_doctor():

    # GET LOGGED-IN USER DETAILS

    user = session.get_user()

    if user is None:
        print("No active user session!")
        input("\nPress Enter to continue...")
        return

    clear_screen()

    width = shutil.get_terminal_size().columns
    width = max(width, 75)

    # HEADER

    print("HOSPITAL MANAGEMENT SYSTEM".center(width))
    print("HOSPITAL ADMINISTRATION PORTAL".center(width))

    # LOGGED-IN USER DETAILS

    print(f"Welcome, {user['name']}!".rjust(width - 2))
    print(f"Role: {user['role']}".rjust(width - 2))

    # MENU HEADING

    print()
    print(("=" * 30).center(width))
    print("USER CREATION".center(width))
    print(("=" * 30).center(width))

    # USER TYPE

    print("\n--- SELECT USER TYPE ---")

    print("1. Doctor")
    print("2. Nurse")
    print("3. Admin")
    print("4. Manager")
    print("5. Receptionist")
    print("6. Pharmacist")

    usertype = input("\nEnter User Type: ").strip().lower()

    # DOCTOR

    if usertype == "1" or usertype == "doctor":

        usertype = "Doctor"

        print("\n--- DOCTOR DETAILS ---")

        name = get_input("Enter Doctor Name")
        specialization = get_input("Enter Doctor Specialization")
        contact = get_input("Enter Doctor Contact Number")
        email = get_input("Enter Doctor Email")

    # NURSE

    elif usertype == "2" or usertype == "nurse":

        usertype = "Nurse"

        print("\n--- NURSE DETAILS ---")

        name = get_input("Enter Nurse Name")
        specialization = get_input("Enter Nurse Department")
        contact = get_input("Enter Nurse Contact Number")
        email = get_input("Enter Nurse Email")

    # ADMIN

    elif usertype == "3" or usertype == "admin":

        usertype = "Admin"

        print("\n--- ADMIN DETAILS ---")

        name = get_input("Enter Admin Name")
        specialization = get_input("Enter Admin Department")
        contact = get_input("Enter Admin Contact Number")
        email = get_input("Enter Admin Email")

    # MANAGER

    elif usertype == "4" or usertype == "manager":

        usertype = "Manager"

        print("\n--- MANAGER DETAILS ---")

        name = get_input("Enter Manager Name")
        specialization = get_input("Enter Manager Department")
        contact = get_input("Enter Manager Contact Number")
        email = get_input("Enter Manager Email")

    # RECEPTIONIST

    elif usertype == "5" or usertype == "receptionist":

        usertype = "Receptionist"

        print("\n--- RECEPTIONIST DETAILS ---")

        name = get_input("Enter Receptionist Name")
        specialization = get_input("Enter Receptionist Department")
        contact = get_input("Enter Receptionist Contact Number")
        email = get_input("Enter Receptionist Email")

    # PHARMACIST

    elif usertype == "6" or usertype == "pharmacist":

        usertype = "Pharmacist"

        print("\n--- PHARMACIST DETAILS ---")

        name = get_input("Enter Pharmacist Name")
        specialization = get_input("Enter Pharmacist Department")
        contact = get_input("Enter Pharmacist Contact Number")
        email = get_input("Enter Pharmacist Email")

    else:

        print("\nInvalid User Type!")
        input("\nPress Enter to return...")
        return

    # DISPLAY ENTERED DETAILS

    print("\n--- USER DETAILS ---")

    print(f"User Type       : {usertype}")
    print(f"Name            : {name}")
    print(f"Department      : {specialization}")
    print(f"Contact Number  : {contact}")
    print(f"Email           : {email}")

    # SUCCESS MESSAGE

    print("\nUser Details Collected Successfully!".center(width))

    # DATABASE INSERTION WILL BE ADDED HERE

    input("\nPress Enter to return to the main menu...")

    # Return to option_display automatically
