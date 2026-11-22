import os
import shutil
from database.dbutility import (
    add_staff,
    get_all_staff,
    update_staff_status
)
from modules import session


def staff_management():

    user = session.get_user()

    width = shutil.get_terminal_size().columns
    width = max(width, 75)
    
    if not user or user["role"].lower() not in ("admin", "manager"):
        print("Access denied!")
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
# HEADER
    
        print("HOSPITAL MANAGEMENT SYSTEM".center(width))
        print("HOSPITAL ADMINISTRATION PORTAL".center(width))
                # LOGGED-IN USER DETAILS
    
        print(f"Welcome, {user['name']}!".rjust(width - 2))
        print(f"Role: {user['role']}".rjust(width - 2))

        print(("=" * 50).center(width))
        print("STAFF MANAGEMENT".center(width))
        print(("=" * 50).center(width))

        print("1. Register Staff")
        print("2. View All Staff")
        print("3. Activate / Deactivate Staff")
        print("4. Return")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            try:
                name = input("Full Name: ").strip()
                password = input("Temporary Password: ")
                role = input("Role: ").strip()
                age = int(input("Age: "))
                gender = input("Gender: ").strip()
                address = input("Address: ").strip()
                mobile = input("Mobile Number: ").strip()
                experience = int(input("Experience (years): "))

                print("\n1. Full-Time")
                print("2. Part-Time")
                print("3. Contract")
                print("4. Visiting")

                employment = {
                    "1": "Full-Time",
                    "2": "Part-Time",
                    "3": "Contract",
                    "4": "Visiting"
                }.get(input("Employment Type: ").strip())

                if employment is None:
                    print("Invalid employment type!")
                    input("\nPress Enter...")
                    continue

                specialty = input("Specialty (optional): ").strip() or None
                joining_date = input("Joining Date (YYYY-MM-DD): ").strip()
                salary = input("Monthly Salary: ").strip()

                data = (
                    name, password, role, age, gender, address,
                    mobile, experience, employment, specialty,
                    joining_date, salary
                )

                staff_id = add_staff(data)

                if staff_id:
                    print(f"Staff registered. User ID: {staff_id}")
                else:
                    print("Staff registration failed.")

            except ValueError:
                print("Please enter valid numeric values.")

            input("\nPress Enter...")

        elif choice == "2":
            staff = get_all_staff()

            if staff:
                for person in staff:
                    print("-" * 55)
                    print("User ID :", person["user_id"])
                    print("Name    :", person["name"])
                    print("Role    :", person["role"])
                    print("Mobile  :", person["mobile_no"])
                    print("Experience:", person["experience"])
                    print("Employment:", person["employment_type"])
                    print("Specialty:", person["specialty"])
                    print("Status  :", person["account_status"])
            else:
                print("No staff records found.")

            input("\nPress Enter...")

        elif choice == "3":
            try:
                staff_id = int(input("Staff User ID: "))

                print("1. Activate")
                print("2. Deactivate")

                status = {
                    "1": "Active",
                    "2": "Inactive"
                }.get(input("Select option: ").strip())

                if status and update_staff_status(staff_id, status):
                    print("Staff status updated.")
                else:
                    print("Unable to update staff status.")

            except ValueError:
                print("Invalid staff ID.")

            input("\nPress Enter...")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")
            input("\nPress Enter...")