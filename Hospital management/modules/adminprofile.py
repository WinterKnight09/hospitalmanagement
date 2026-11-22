import os
import shutil
from database.dbutility import (
    get_admin_profile,
    update_admin_profile,
    change_user_password
)
from modules import session


def admin_profile():

    user = session.get_user()

    width = shutil.get_terminal_size().columns
    width = max(width, 75)

    if not user or user["role"].lower() != "admin":
        print("Admin access only!")
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
        print("ADMIN PROFILE MANAGEMENT".center(width))
        print(("=" * 50).center(width))

        print("1. View Profile")
        print("2. Update Profile")
        print("3. Change Password")
        print("4. Return")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            profile = get_admin_profile(user["user_id"])

            if profile:
                for key, value in profile.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print("Profile not found.")

            input("\nPress Enter...")

        elif choice == "2":
            name = input("New Name: ").strip()
            mobile = input("New Mobile Number: ").strip()
            address = input("New Address: ").strip()

            if update_admin_profile(
                user["user_id"], name, mobile, address
            ):
                user["name"] = name
                session.set_user(user)
                print("Profile updated successfully.")
            else:
                print("Profile update failed.")

            input("\nPress Enter...")

        elif choice == "3":
            old_password = input("Current Password: ")
            new_password = input("New Password: ")
            confirm = input("Confirm New Password: ")

            if new_password != confirm:
                print("Passwords do not match!")

            elif len(new_password) < 8:
                print("Password must contain at least 8 characters.")

            elif change_user_password(
                user["user_id"], old_password, new_password
            ):
                print("Password changed successfully.")

            else:
                print("Password change failed.")

            input("\nPress Enter...")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")
            input("\nPress Enter...")