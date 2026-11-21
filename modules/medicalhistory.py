
# PATIENT MEDICAL HISTORY

import os
from modules import session


def medicalhistory():

    user = session.get_user()

    if user is None:
        print("No active user session!")
        return

    os.system('cls' if os.name == 'nt' else 'clear')

    print("HOSPITAL MANAGEMENT SYSTEM")
    print("HOSPITAL ADMINISTRATION PORTAL")

    print(f"\nWelcome, {user['name']}!")
    print(f"Role: {user['role']}")

    print("\n================================")
    print("PATIENT MEDICAL HISTORY")
    print("================================")

    # YOUR MEDICAL HISTORY CODE GOES HERE

    print("\nMedical History Module")

    input("\nPress Enter to return to the main menu...")

    # Return to option_display automatically
