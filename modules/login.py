
import os
import shutil
import msvcrt

from database.dbutility import login_verify


# Clear terminal screen
def clear_screen():
    os.system('cls')


# Password input with show/hide feature
def password_input(start, width):

    password = ""
    show_password = False

    print(" " * start + "Password".ljust(20), end=": ", flush=True)

    while True:

        char = msvcrt.getwch()

        # Enter key
        if char == '\r':
            print()
            break

        # Backspace
        elif char == '\b':
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)

        # Function keys
        elif char in ('\x00', '\xe0'):
            key = msvcrt.getwch()

            # F2 - Show/Hide password
            if key == '\x3c':

                show_password = not show_password

                # Refresh password display
                print('\r' + ' ' * width + '\r', end='', flush=True)

                print(
                    " " * start + "Password".ljust(20),
                    end=": ",
                    flush=True
                )

                for c in password:
                    print(
                        c if show_password else '*',
                        end='',
                        flush=True
                    )

        # Normal characters
        else:
            password += char

            print(
                char if show_password else '*',
                end='',
                flush=True
            )

    return password


# Login function
def logins():

    attempts = 3

    while attempts > 0:

        clear_screen()

        width = shutil.get_terminal_size().columns

        print("\n")
        print(
            "Welcome to the Hospital Management System".center(width)
        )
        print("Login to continue".center(width))
        print("\n")

        label_width = 20
        total_width = label_width + 25
        start = max(0, (width - total_width) // 2)

        # User ID
        try:
            print(
                " " * start + "User ID".ljust(label_width),
                end=": "
            )
            user_id = int(input())

        except ValueError:
            user_id = None

        # Username
        print(
            " " * start + "Username".ljust(label_width),
            end=": "
        )
        username = input()

        # Password
        password = password_input(start, width)

        # Verify login
        if user_id is not None:
            verify = login_verify(user_id, username, password)
        else:
            verify = None

        # Successful login
        if verify:

            clear_screen()

            print("\n")
            print("Login verified!".center(width))
            print("Welcome to the Hospital Management System".center(width))

            input("\nPress Enter to continue...")

            clear_screen()

            return verify

        # Failed login
        else:

            attempts -= 1

            clear_screen()

            print("\n")
            print(
                "Invalid User ID, Username or Password!".center(width)
            )

            if attempts > 0:

                print("\n")
                print(
                    f"{attempts} attempt(s) remaining".center(width)
                )

                input("\nPress Enter to try again...")

            else:

                print("\n")
                print(
                    "Maximum login attempts exceeded!".center(width)
                )
                print(
                    "Exiting Hospital Management System...".center(width)
                )

                return None
