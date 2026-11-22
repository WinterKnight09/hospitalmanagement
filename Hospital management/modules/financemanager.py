import os
import shutil
from database.dbutility import get_finance_summary, get_all_bills
from modules import session



def finance_manager():

    user = session.get_user()
    
    width = shutil.get_terminal_size().columns
    width = max(width, 75)
    

    if not user or user["role"].lower() not in (
        "manager", "admin", "accountant"
    ):
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

        print(("=" * 55).center(width))
        print("FINANCE MANAGER MODULE".center(width))
        print(("=" * 55).center(width))

        print("1. Financial Dashboard")
        print("2. View All Bills")
        print("3. Return to Main Menu")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            data = get_finance_summary()

            if data:
                print("\nFINANCIAL SUMMARY")
                print("-" * 40)
                print("Total Bills          :", data["total_bills"])
                print("Total Billed         :", data["total_billed"])
                print("Verified Collections :", data["verified_collections"])
                print("Outstanding Amount   :", data["outstanding_amount"])

            input("\nPress Enter to continue...")

        elif choice == "2":
            bills = get_all_bills()

            if bills:
                print("\nALL PATIENT BILLS")
                print("-" * 90)

                for bill in bills:
                    print(
                        f"Bill: {bill['invoice_number']} | "
                        f"Patient: {bill['patient_name']} | "
                        f"Amount: {bill['total_amount']} | "
                        f"Status: {bill['payment_status']}"
                    )
            else:
                print("No bills found.")

            input("\nPress Enter to continue...")

        elif choice == "3":
            break

        else:
            print("Invalid choice!")
            input("\nPress Enter...")