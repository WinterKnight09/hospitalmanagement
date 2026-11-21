
# SESSION MANAGEMENT

current_user = None


def set_user(user):
    global current_user
    current_user = user


def get_user():
    return current_user


def clear_user():
    global current_user
    current_user = None
