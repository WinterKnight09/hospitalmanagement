import os
import shutil
from database.dbutility import (
    add_duty,
    get_duty_schedule,
    update_duty_status
)
from modules import session

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def duty_management():

    user = session.get_user()
    width = shutil.get_terminal_size().columns
    width = max(width, 75)
    if user is None:
        print("No active user session!")
        input("\nPress Enter to continue...")
        return
    

    if not user or user["role"].lower() not in (
        "admin", "manager", "head nurse"
    ):
        print("Access denied!")
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
    
    
        print("HOSPITAL MANAGEMENT SYSTEM".center(width))
        print("HOSPITAL ADMINISTRATION PORTAL".center(width))
                # LOGGED-IN USER DETAILS
    
        print(f"Welcome, {user['name']}!".rjust(width - 2))
        print(f"Role: {user['role']}".rjust(width - 2))


        print("=" * 50)
        print("          DUTY MANAGEMENT")
        print("=" * 50)

        print("1. Schedule Duty")
        print("2. View All Duties")
        print("3. View Duties by Date")
        print("4. Update Duty Status")
        print("5. Return")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            try:
                staff_id = int(input("Staff User ID: "))
                date = input("Duty Date (YYYY-MM-DD): ").strip()

                print("\n1. Morning")
                print("2. Evening")
                print("3. Night")

                shifts = {
                    "1": "Morning",
                    "2": "Evening",
                    "3": "Night"
                }

                shift = shifts.get(input("Select Shift: ").strip())

                if shift is None:
                    print("Invalid shift!")
                    input("\nPress Enter...")
                    continue

                start = input("Start Time (HH:MM:SS): ").strip()
                end = input("End Time (HH:MM:SS): ").strip()
                department = input("Department: ").strip()

                duty_id = add_duty(
                    staff_id,
                    date,
                    shift,
                    start,
                    end,
                    department,
                    user["user_id"]
                )

                if duty_id:
                    print(f"Duty scheduled. Duty ID: {duty_id}")

            except ValueError:
                print("Invalid input!")

            input("\nPress Enter...")

        elif choice in ("2", "3"):
            date = None

            if choice == "3":
                date = input("Enter Date (YYYY-MM-DD): ").strip()

            duties = get_duty_schedule(date)

            if duties:
                for duty in duties:
                    print("-" * 55)
                    print("Duty ID :", duty["duty_id"])
                    print("Staff   :", duty["name"])
                    print("Role    :", duty["role"])
                    print("Date    :", duty["duty_date"])
                    print("Shift   :", duty["shift"])
                    print("Time    :", duty["start_time"], "-", duty["end_time"])
                    print("Department:", duty["department"])
                    print("Status  :", duty["duty_status"])
            else:
                print("No duty records found.")

            input("\nPress Enter...")

        elif choice == "4":
            try:
                duty_id = int(input("Duty ID: "))

                print("1. Completed")
                print("2. Cancelled")

                status = {
                    "1": "Completed",
                    "2": "Cancelled"
                }.get(input("Select status: ").strip())

                if status and update_duty_status(duty_id, status):
                    print("Duty status updated.")
                else:
                    print("Unable to update duty.")

            except ValueError:
                print("Invalid duty ID.")

            input("\nPress Enter...")

        elif choice == "5":
            break

        else:
            print("Invalid choice!")
            input("\nPress Enter...")