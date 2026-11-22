import os
import shutil
from database.dbutility import (
    save_payment,
    verify_payment,
    get_payment_receipt
)
from modules import session


def payment_verification():

    user = session.get_user()

    width = shutil.get_terminal_size().columns
    width = max(width, 75)

    if not user or user["role"].lower() not in (
        "manager", "admin", "accountant", "billing clerk"
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
        print("PAYMENT VERIFICATION AND RECEIPTS".center(width))
        print(("=" * 55).center(width))

        print("1. Record Payment")
        print("2. Verify Payment")
        print("3. Generate Receipt")
        print("4. Return")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            try:
                bill_id = int(input("Enter Bill ID: "))
                amount = input("Payment Amount: ")

                print("\n1. Cash")
                print("2. UPI")
                print("3. Card")
                print("4. Bank Transfer")

                methods = {
                    "1": "Cash",
                    "2": "UPI",
                    "3": "Card",
                    "4": "Bank Transfer"
                }

                method = methods.get(input("Select method: ").strip())

                if method is None:
                    print("Invalid payment method!")
                    input("\nPress Enter...")
                    continue

                reference = input(
                    "Transaction Reference (optional): "
                ).strip() or None

                payment_id = save_payment(
                    bill_id, amount, method, reference
                )

                if payment_id:
                    print(f"\nPayment recorded. Payment ID: {payment_id}")
                    print("Status: Pending Verification")

            except ValueError:
                print("Invalid bill ID or amount.")

            input("\nPress Enter to continue...")

        elif choice == "2":
            try:
                payment_id = int(input("Enter Payment ID: "))

                print("1. Verify")
                print("2. Reject")

                action = input("Select action: ").strip()

                if action not in ("1", "2"):
                    print("Invalid choice!")
                else:
                    result = verify_payment(
                        payment_id,
                        user["user_id"],
                        approve=(action == "1")
                    )

                    print(
                        "Payment updated successfully."
                        if result else "Payment verification failed."
                    )

            except ValueError:
                print("Invalid payment ID.")

            input("\nPress Enter to continue...")

        elif choice == "3":
            try:
                payment_id = int(input("Enter Payment ID: "))
                receipt = get_payment_receipt(payment_id)

                if receipt:
                    print("\n" + "=" * 50)
                    print("             PAYMENT RECEIPT")
                    print("=" * 50)
                    print("Receipt ID :", receipt["payment_id"])
                    print("Invoice    :", receipt["invoice_number"])
                    print("Patient    :", receipt["patient_name"])
                    print("Patient ID :", receipt["patient_id"])
                    print("Amount     :", receipt["amount"])
                    print("Method     :", receipt["payment_method"])
                    print("Reference  :", receipt["transaction_reference"])
                    print("Date       :", receipt["payment_date"])
                    print("Verified by:", receipt["verified_by"])
                    print("Status     :", receipt["verification_status"])
                    print("=" * 50)

                else:
                    print("Verified receipt not found.")

            except ValueError:
                print("Invalid payment ID.")

            input("\nPress Enter to continue...")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")
            input("\nPress Enter...")