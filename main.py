
# HOSPITAL MANAGEMENT SYSTEM
# MAIN APPLICATION

from modules.login import logins
from modules.optiondisplay import option_display
from modules import session


login_result = logins()

if login_result:

    session.set_user(login_result)

    option_display()

else:
    print("Login failed.")
