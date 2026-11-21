
from database.dbconnector import get_connector


def login_verify(user_id, username, password):

    mydb = get_connector()

    if mydb is None:
        return None

    cursor = mydb.cursor(dictionary=True)

    query = """
        SELECT user_id, name, role
        FROM app_users
        WHERE user_id = %s
        AND name = %s
        AND password = %s
    """

    values = (user_id, username, password)

    cursor.execute(query, values)

    result = cursor.fetchone()

    cursor.close()
    mydb.close()

    return result
def add_patient(patient_data):
    mydb = get_connector()

    if mydb is None:
        return False

    cursor = mydb.cursor()

    query = """
        INSERT INTO patients (name, dob, age, gender, profession, income, address, mobile_number, secondary_number, email, emergency_contact, id_proof, id_proof_number, blood_group, patient_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, tuple(patient_data))

    mydb.commit()
    cursor.close()
    mydb.close()

    return True

def save_patient(patient_data):
    
    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor()

        query = """
            INSERT INTO PATIENT_REGISTRATION (
                patient_name,
                dob,
                age,
                gender,
                profession,
                income,
                address,
                mobile_number,
                secondary_number,
                email,
                emergency_contact,
                id_proof,
                id_proof_number,
                blood_group,
                patient_type
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        cursor.execute(query, patient_data)

        patient_id = cursor.lastrowid

        patient_code = f"P{patient_id:04d}"

        cursor.execute(
            """
            UPDATE patients
            SET patient_code = %s
            WHERE patient_id = %s
            """,
            (patient_code, patient_id)
        )

        connection.commit()

        return patient_id, patient_code

    except Exception as error:

        connection.rollback()
        print("Patient Save Error:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


# GET ALL PATIENTS

def get_all_patients():

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM PATIENT_REGISTRATION
            ORDER BY patient_id
        """)

        return cursor.fetchall()

    except Exception as error:

        print("Database Error:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


# GET PATIENT BY NAME

def get_patient_by_name(name):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM PATIENT_REGISTRATION
            WHERE patient_name LIKE %s
            ORDER BY patient_name
        """, (f"%{name}%",))

        return cursor.fetchall()

    except Exception as error:

        print("Database Error:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()


# GET PATIENT BY ID OR CODE

def get_patient_by_id(patient_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM PATIENT_REGISTRATION
            WHERE patient_id = %s
               OR patient_code = %s
        """, (patient_id, patient_id))

        return cursor.fetchone()

    except Exception as error:

        print("Database Error:", error)
        return None

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()