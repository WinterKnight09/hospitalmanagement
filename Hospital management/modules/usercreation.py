
# USER CREATION MODULE

import os
import shutil
from modules import session


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(label, length=35):
    return input(f"{label.ljust(length)}: ")


def user_creation():

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

    usertype = input("\nEnter User Type: ").strip().lower()

    # DOCTOR

    if usertype == "1" or usertype == "doctor":

        usertype = "Doctor"

        print("\n--- DOCTOR DETAILS ---")

        name = get_input("Enter Doctor Name")
        specialization = get_input("Enter Doctor Specialization")
        license_number = get_input("Enter Doctor License Number")
        qualification = get_input("Enter Doctor Qualification")
        experience = get_input("Enter Doctor Experience")
        identity_proof = get_input("Enter Doctor Identity Proof(Aadhaar/Passport/Driving License/pan card)").strip()
        if identity_proof.lower() == "aadhaar" or identity_proof.lower() == "Aadhaar":
            Aadhaar_number = get_input("Enter Doctor Aadhaar Number")
        elif identity_proof.lower() == "passport" or identity_proof.lower() == "Passport":
            passport_number = get_input("Enter Doctor Passport Number")    
        elif identity_proof.lower() == "driving license" or identity_proof.lower() == "Driving License":
            driving_license_number = get_input("Enter Doctor Driving License Number")
        elif identity_proof.lower() == "pan card" or identity_proof.lower() == "Pan Card":
            pan_card_number = get_input("Enter Doctor Pan Card Number")
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
        if identity_proof.lower() == "aadhaar" or identity_proof.lower() == "Aadhaar":
            Aadhaar_number = get_input("Enter Nurse Aadhaar Number")
        elif identity_proof.lower() == "passport" or identity_proof.lower() == "Passport":
            passport_number = get_input("Enter Nurse Passport Number")    
        elif identity_proof.lower() == "driving license" or identity_proof.lower() == "Driving License":
            driving_license_number = get_input("Enter Nurse Driving License Number")
        elif identity_proof.lower() == "pan card" or identity_proof.lower() == "Pan Card":
            pan_card_number = get_input("Enter Nurse Pan Card Number")
        contact = get_input("Enter Nurse Contact Number")
        email = get_input("Enter Nurse Email")

    # ADMIN

    elif usertype == "3" or usertype == "admin":

        usertype = "Admin"

        print("\n--- ADMIN DETAILS ---")

        name = get_input("Enter admin Name")
        specialization = get_input("Enter admin Specialization")
        license_number = get_input("Enter admin License Number")
        qualification = get_input("Enter admin Qualification")
        experience = get_input("Enter admin Experience")
        identity_proof = get_input("Enter admin Identity Proof(Aadhaar/Passport/Driving License/pan card)").strip()
        if identity_proof.lower() == "aadhaar" or identity_proof.lower() == "Aadhaar":
            Aadhaar_number = get_input("Enter admin Aadhaar Number")
        elif identity_proof.lower() == "passport" or identity_proof.lower() == "Passport":
            passport_number = get_input("Enter admin Passport Number")    
        elif identity_proof.lower() == "driving license" or identity_proof.lower() == "Driving License":
            driving_license_number = get_input("Enter admin Driving License Number")
        elif identity_proof.lower() == "pan card" or identity_proof.lower() == "Pan Card":
            pan_card_number = get_input("Enter admin Pan Card Number")
        contact = get_input("Enter admin Contact Number")
        email = get_input("Enter admin Email")

    # MANAGER

    elif usertype == "4" or usertype == "manager":

        usertype = "Manager"

        print("\n--- MANAGER DETAILS ---")

        name = get_input("Enter Manager Name")
        specialization = get_input("Enter Manager Department")
        license_number = get_input("Enter Manager License Number")
        qualification = get_input("Enter Manager Qualification")
        experience = get_input("Enter Manager Experience")
        identity_proof = get_input("Enter Manager Identity Proof(Aadhaar/Passport/Driving License/pan card)").strip()
        if identity_proof.lower() == "aadhaar" or identity_proof.lower() == "Aadhaar":
            Aadhaar_number = get_input("Enter Manager Aadhaar Number")
        elif identity_proof.lower() == "passport" or identity_proof.lower() == "Passport":
            passport_number = get_input("Enter Manager Passport Number")    
        elif identity_proof.lower() == "driving license" or identity_proof.lower() == "Driving License":
            driving_license_number = get_input("Enter Manager Driving License Number")
        elif identity_proof.lower() == "pan card" or identity_proof.lower() == "Pan Card":
            pan_card_number = get_input("Enter Manager Pan Card Number")
        contact = get_input("Enter Manager Contact Number")
        email = get_input("Enter Manager Email")

    # RECEPTIONIST

    elif usertype == "5" or usertype == "receptionist":

        usertype = "Receptionist"

        print("\n--- RECEPTIONIST DETAILS ---")

        name = get_input("Enter Receptionist Name")
        specialization = get_input("Enter Receptionist Department")
        qualification = get_input("Enter Receptionist Qualification")
        experience = get_input("Enter Receptionist Experience")
        contact = get_input("Enter Receptionist Contact Number")
        email = get_input("Enter Receptionist Email")
        identity_proof = get_input("Enter Receptionist Identity Proof(Aadhaar/Passport/Driving License/pan card)").strip()
        if identity_proof.lower() == "aadhaar" or identity_proof.lower() == "Aadhaar":
            Aadhaar_number = get_input("Enter Receptionist Aadhaar Number")
        elif identity_proof.lower() == "passport" or identity_proof.lower() == "Passport":
            passport_number = get_input("Enter Receptionist Passport Number")    
        elif identity_proof.lower() == "driving license" or identity_proof.lower() == "Driving License":
            driving_license_number = get_input("Enter Receptionist Driving License Number")
        elif identity_proof.lower() == "pan card" or identity_proof.lower() == "Pan Card":
            pan_card_number = get_input("Enter Receptionist Pan Card Number")
        contact = get_input("Enter Receptionist Contact Number")
        email = get_input("Enter Receptionist Email")
    else:

        print("\nInvalid User Type!")
        input("\nPress Enter to return...")
        return

    # SUCCESS MESSAGE

    print("\nUser Details Collected Successfully!".center(width))

    # DATABASE INSERTION WILL BE ADDED HERE

    input("\nPress Enter to return to the main menu...")

    # Return to option_display automatically
