from decimal import Decimal, InvalidOperation
from database.dbconnector import get_connector


# ============================================================
# COMMON DATABASE HELPERS
# ============================================================

def _close_database(connection, cursor):
    if cursor is not None:
        try:
            cursor.close()
        except Exception:
            pass

    if connection is not None:
        try:
            connection.close()
        except Exception:
            pass


def _add_patient_code(patient):
    if patient:
        patient["patient_code"] = f"P{patient['patient_id']:04d}"
    return patient


def _add_patient_codes(patients):
    return [_add_patient_code(patient) for patient in patients]


def _get_patient_id(value):
    try:
        value = str(value).strip().upper()

        if value.startswith("P"):
            value = value[1:]

        patient_id = int(value)

        return patient_id if patient_id > 0 else None

    except (ValueError, TypeError):
        return None


# ============================================================
# USER LOGIN
# ============================================================

def login_verify(user_id, username, password):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, name, role
            FROM app_users
            WHERE user_id = %s
              AND name = %s
              AND password = %s
        """, (user_id, username, password))

        return cursor.fetchone()

    except Exception as error:
        print("Login Verification Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# PATIENT REGISTRATION
# ============================================================

def save_patient(patient_data):
    """
    Expected order:

    0  patient_name
    1  dob
    2  age
    3  gender
    4  profession
    5  income
    6  address
    7  mobile_number
    8  secondary_number
    9  email
    10 emergency_contact
    11 id_proof_type
    12 id_proof_number
    13 blood_group
    14 patient_type
    """

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        if len(patient_data) != 15:
            raise ValueError("Patient data must contain exactly 15 values.")

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patient_registration (
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
                id_proof_type,
                id_proof_number,
                blood_group,
                patient_type
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, tuple(patient_data))

        patient_id = cursor.lastrowid

        connection.commit()

        return patient_id, f"P{patient_id:04d}"

    except Exception as error:
        connection.rollback()
        print("Patient Save Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


def add_patient(patient_data):
    return save_patient(patient_data) is not None


# ============================================================
# PATIENT RETRIEVAL
# ============================================================

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
            FROM patient_registration
            ORDER BY patient_id
        """)

        return _add_patient_codes(cursor.fetchall())

    except Exception as error:
        print("Get All Patients Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


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
            FROM patient_registration
            WHERE patient_name LIKE %s
            ORDER BY patient_name
        """, (f"%{name.strip()}%",))

        return _add_patient_codes(cursor.fetchall())

    except Exception as error:
        print("Patient Name Search Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


def get_patient_by_id(patient_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        numeric_id = _get_patient_id(patient_id)

        if numeric_id is None:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM patient_registration
            WHERE patient_id = %s
        """, (numeric_id,))

        return _add_patient_code(cursor.fetchone())

    except Exception as error:
        print("Patient ID Search Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# DOCTOR PROFILE
# ============================================================

def get_doctor_profile(user_id):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                d.doctor_id,
                d.user_id,
                d.department,
                d.specialization,
                u.name
            FROM doctors d
            JOIN app_users u
                ON d.user_id = u.user_id
            WHERE d.user_id = %s
        """, (user_id,))

        return cursor.fetchone()

    except Exception as error:
        print("Doctor Profile Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# GET ALL DOCTORS
# ============================================================

def get_all_doctors():
    db = get_connector()

    if db is None:
        return None

    cursor = None

    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                d.user_id AS doctor_id,
                u.name AS name,
                d.department AS department,
                d.specialization AS specialization
            FROM doctors d
            JOIN app_users u ON d.user_id = u.user_id
            ORDER BY u.name
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        print("Error fetching doctors:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        db.close()
def get_dashboard_counts(doctor_id=None):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        if doctor_id is None:

            cursor.execute("""
                SELECT COUNT(*) AS total_patients
                FROM patient_registration
            """)

            patients = cursor.fetchone()

            cursor.execute("""
                SELECT COUNT(*) AS total_consultations
                FROM consultations
            """)

            consultations = cursor.fetchone()

        else:

            cursor.execute("""
                SELECT COUNT(DISTINCT patient_id) AS total_patients
                FROM patient_assignments
                WHERE doctor_id = %s
                  AND status = 'Active'
            """, (doctor_id,))

            patients = cursor.fetchone()

            cursor.execute("""
                SELECT COUNT(*) AS total_consultations
                FROM consultations
                WHERE doctor_id = %s
            """, (doctor_id,))

            consultations = cursor.fetchone()

        return {
            "total_patients": patients["total_patients"],
            "total_consultations": consultations["total_consultations"]
        }

    except Exception as error:
        print("Dashboard Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# ASSIGNED PATIENTS
# doctor_id=None returns all registered patients.
# ============================================================

def get_assigned_patients(doctor_id=None):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        if doctor_id is None:

            cursor.execute("""
                SELECT
                    p.patient_id,
                    p.patient_name,
                    p.age,
                    p.gender,
                    p.patient_type,
                    p.blood_group,
                    GROUP_CONCAT(
                        DISTINCT u.name
                        ORDER BY u.name
                        SEPARATOR ', '
                    ) AS doctor_names,
                    MAX(pa.assigned_date) AS assigned_date
                FROM patient_registration p
                LEFT JOIN patient_assignments pa
                    ON pa.patient_id = p.patient_id
                   AND pa.status = 'Active'
                LEFT JOIN doctors d
                    ON d.doctor_id = pa.doctor_id
                LEFT JOIN app_users u
                    ON u.user_id = d.user_id
                GROUP BY
                    p.patient_id,
                    p.patient_name,
                    p.age,
                    p.gender,
                    p.patient_type,
                    p.blood_group
                ORDER BY p.patient_name
            """)

        else:

            cursor.execute("""
                SELECT
                    p.patient_id,
                    p.patient_name,
                    p.age,
                    p.gender,
                    p.patient_type,
                    p.blood_group,
                    pa.assigned_date
                FROM patient_assignments pa
                JOIN patient_registration p
                    ON p.patient_id = pa.patient_id
                WHERE pa.doctor_id = %s
                  AND pa.status = 'Active'
                ORDER BY p.patient_name
            """, (doctor_id,))

        return _add_patient_codes(cursor.fetchall())

    except Exception as error:
        print("Assigned Patient Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# PATIENT SEARCH
# doctor_id=None searches all patients.
# ============================================================

def get_patient_for_doctor(doctor_id, search_value):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        search_value = str(search_value).strip()
        numeric_id = _get_patient_id(search_value)

        cursor = connection.cursor(dictionary=True)

        if doctor_id is None:

            cursor.execute("""
                SELECT
                    p.patient_id,
                    p.patient_name,
                    p.age,
                    p.gender,
                    p.patient_type,
                    p.blood_group
                FROM patient_registration p
                WHERE p.patient_name LIKE %s
                   OR p.patient_id = %s
                ORDER BY p.patient_name
            """, (
                f"%{search_value}%",
                numeric_id if numeric_id is not None else -1
            ))

        else:

            cursor.execute("""
                SELECT DISTINCT
                    p.patient_id,
                    p.patient_name,
                    p.age,
                    p.gender,
                    p.patient_type,
                    p.blood_group
                FROM patient_assignments pa
                JOIN patient_registration p
                    ON p.patient_id = pa.patient_id
                WHERE pa.doctor_id = %s
                  AND pa.status = 'Active'
                  AND (
                        p.patient_name LIKE %s
                        OR p.patient_id = %s
                  )
                ORDER BY p.patient_name
            """, (
                doctor_id,
                f"%{search_value}%",
                numeric_id if numeric_id is not None else -1
            ))

        return _add_patient_codes(cursor.fetchall())

    except Exception as error:
        print("Patient Search Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# SAVE CONSULTATION
# Patient must be actively assigned to selected doctor.
# ============================================================

def save_consultation(
    doctor_id,
    patient_id,
    symptoms,
    observations,
    diagnosis,
    treatment_plan,
    notes
):

    connection = get_connector()

    if connection is None:
        return False

    cursor = None

    try:
        numeric_id = _get_patient_id(patient_id)

        if numeric_id is None:
            print("Invalid patient ID.")
            return False

        if doctor_id is None:
            print("A responsible doctor must be selected.")
            return False

        cursor = connection.cursor()

        cursor.execute("""
            SELECT assignment_id
            FROM patient_assignments
            WHERE doctor_id = %s
              AND patient_id = %s
              AND status = 'Active'
            LIMIT 1
        """, (doctor_id, numeric_id))

        if cursor.fetchone() is None:
            print("The patient is not actively assigned to this doctor.")
            return False

        cursor.execute("""
            INSERT INTO consultations (
                patient_id,
                doctor_id,
                symptoms,
                observations,
                diagnosis,
                treatment_plan,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            numeric_id,
            doctor_id,
            symptoms,
            observations,
            diagnosis,
            treatment_plan,
            notes
        ))

        connection.commit()

        return True

    except Exception as error:
        connection.rollback()
        print("Consultation Save Error:", error)
        return False

    finally:
        _close_database(connection, cursor)


# ============================================================
# PATIENT CONSULTATION HISTORY
# doctor_id=None returns all doctors' consultations.
# ============================================================

def get_patient_consultations(doctor_id, patient_id):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        numeric_id = _get_patient_id(patient_id)

        if numeric_id is None:
            return None

        cursor = connection.cursor(dictionary=True)

        if doctor_id is None:

            cursor.execute("""
                SELECT
                    c.consultation_id,
                    c.patient_id,
                    c.doctor_id,
                    c.symptoms,
                    c.observations,
                    c.diagnosis,
                    c.treatment_plan,
                    c.notes,
                    c.consultation_date,
                    u.name AS doctor_name,
                    d.department
                FROM consultations c
                LEFT JOIN doctors d
                    ON d.doctor_id = c.doctor_id
                LEFT JOIN app_users u
                    ON u.user_id = d.user_id
                WHERE c.patient_id = %s
                ORDER BY c.consultation_date DESC
            """, (numeric_id,))

        else:

            cursor.execute("""
                SELECT
                    c.consultation_id,
                    c.patient_id,
                    c.doctor_id,
                    c.symptoms,
                    c.observations,
                    c.diagnosis,
                    c.treatment_plan,
                    c.notes,
                    c.consultation_date,
                    u.name AS doctor_name,
                    d.department
                FROM consultations c
                LEFT JOIN doctors d
                    ON d.doctor_id = c.doctor_id
                LEFT JOIN app_users u
                    ON u.user_id = d.user_id
                WHERE c.doctor_id = %s
                  AND c.patient_id = %s
                ORDER BY c.consultation_date DESC
            """, (doctor_id, numeric_id))

        return cursor.fetchall()

    except Exception as error:
        print("Consultation History Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


# ============================================================
# BILLING
# ============================================================

def get_patient_for_billing(patient_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        patient_id = _get_patient_id(patient_id)

        if patient_id is None:
            print("Invalid patient ID.")
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                patient_id,
                patient_name,
                mobile_number,
                patient_type
            FROM patient_registration
            WHERE patient_id = %s
        """, (patient_id,))

        return cursor.fetchone()

    except Exception as error:
        print("Patient Lookup Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


def save_bill(patient_id, consultation, medicine, tests, user_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        patient_id = _get_patient_id(patient_id)

        if patient_id is None:
            raise ValueError("Invalid patient ID.")

        consultation = Decimal(str(consultation))
        medicine = Decimal(str(medicine))
        tests = Decimal(str(tests))

        amounts = (consultation, medicine, tests)

        if any(
            not amount.is_finite() or amount < 0
            for amount in amounts
        ):
            raise ValueError("Charges must be valid non-negative amounts.")

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT patient_id
            FROM patient_registration
            WHERE patient_id = %s
        """, (patient_id,))

        if cursor.fetchone() is None:
            raise ValueError("Patient does not exist.")

        cursor.execute("""
            SELECT user_id
            FROM app_users
            WHERE user_id = %s
        """, (user_id,))

        if cursor.fetchone() is None:
            raise ValueError("Invalid billing user.")

        total = consultation + medicine + tests

        cursor.execute("""
            INSERT INTO patient_bills (
                patient_id,
                consultation_fee,
                medicine_charges,
                test_charges,
                total_amount,
                created_by
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            consultation,
            medicine,
            tests,
            total,
            user_id
        ))

        bill_id = cursor.lastrowid
        invoice_number = f"BILL-{bill_id:06d}"

        cursor.execute("""
            UPDATE patient_bills
            SET invoice_number = %s
            WHERE bill_id = %s
        """, (invoice_number, bill_id))

        connection.commit()

        return {
            "bill_id": bill_id,
            "invoice_number": invoice_number,
            "patient_id": patient_id,
            "consultation_fee": consultation,
            "medicine_charges": medicine,
            "test_charges": tests,
            "total": total,
            "payment_status": "Pending"
        }

    except (InvalidOperation, ValueError) as error:
        connection.rollback()
        print("Bill Validation Error:", error)
        return None

    except Exception as error:
        connection.rollback()
        print("Bill Save Error:", error)
        return None

    finally:
        _close_database(connection, cursor)


def get_bill_by_id(bill_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                b.bill_id,
                b.invoice_number,
                b.patient_id,
                b.consultation_fee,
                b.medicine_charges,
                b.test_charges,
                b.total_amount,
                b.payment_status,
                b.bill_date,
                b.created_by,
                p.patient_name,
                p.mobile_number,
                u.name AS generated_by
            FROM patient_bills b
            JOIN patient_registration p
                ON p.patient_id = b.patient_id
            LEFT JOIN app_users u
                ON u.user_id = b.created_by
            WHERE b.bill_id = %s
        """, (bill_id,))

        return cursor.fetchone()

    except Exception as error:
        print("Bill Retrieval Error:", error)
        return None

    finally:
        _close_database(connection, cursor)
        
        
# ============================================================
# FINANCE MANAGER
# ============================================================

def get_finance_summary():
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_bills,
                COALESCE(SUM(total_amount), 0) AS total_billed,
                COALESCE(SUM(
                    CASE WHEN payment_status = 'Paid'
                    THEN total_amount ELSE 0 END
                ), 0) AS paid_bills,
                COALESCE(SUM(
                    CASE WHEN payment_status != 'Paid'
                    THEN total_amount ELSE 0 END
                ), 0) AS outstanding_amount
            FROM patient_bills
        """)

        bills = cursor.fetchone()

        cursor.execute("""
            SELECT
                COALESCE(SUM(amount), 0) AS verified_collections
            FROM payment_records
            WHERE verification_status = 'Verified'
        """)

        payments = cursor.fetchone()

        return {
            **bills,
            "verified_collections": payments["verified_collections"]
        }

    except Exception as error:
        print("Finance Summary Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


def get_all_bills():
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                b.bill_id,
                b.invoice_number,
                b.patient_id,
                p.patient_name,
                b.total_amount,
                b.payment_status,
                b.bill_date
            FROM patient_bills b
            JOIN patient_registration p
                ON p.patient_id = b.patient_id
            ORDER BY b.bill_date DESC
        """)
        return cursor.fetchall()

    except Exception as error:
        print("Bill List Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


# ============================================================
# PAYMENT VERIFICATION AND RECEIPTS
# ============================================================

def save_payment(bill_id, amount, method, reference=None):
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        amount = Decimal(str(amount))

        if not amount.is_finite() or amount <= 0:
            raise ValueError("Payment must be greater than zero.")

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT bill_id, total_amount
            FROM patient_bills
            WHERE bill_id = %s
        """, (bill_id,))

        bill = cursor.fetchone()

        if bill is None:
            raise ValueError("Bill not found.")

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS pending_amount
            FROM payment_records
            WHERE bill_id = %s
              AND verification_status IN ('Pending', 'Verified')
        """, (bill_id,))

        recorded = Decimal(str(cursor.fetchone()["pending_amount"]))

        if recorded + amount > Decimal(str(bill["total_amount"])):
            raise ValueError("Payment exceeds the remaining bill amount.")

        cursor.execute("""
            INSERT INTO payment_records (
                bill_id, amount, payment_method,
                transaction_reference
            )
            VALUES (%s, %s, %s, %s)
        """, (bill_id, amount, method, reference))

        payment_id = cursor.lastrowid
        connection.commit()
        return payment_id

    except (InvalidOperation, ValueError) as error:
        connection.rollback()
        print("Payment Error:", error)
        return None
    except Exception as error:
        connection.rollback()
        print("Payment Save Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


def verify_payment(payment_id, verifier_id, approve=True):
    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT payment_id, bill_id, amount, verification_status
            FROM payment_records
            WHERE payment_id = %s
            FOR UPDATE
        """, (payment_id,))

        payment = cursor.fetchone()

        if payment is None or payment["verification_status"] != "Pending":
            raise ValueError("Pending payment not found.")

        status = "Verified" if approve else "Rejected"

        cursor.execute("""
            UPDATE payment_records
            SET verification_status = %s,
                verified_by = %s
            WHERE payment_id = %s
        """, (status, verifier_id, payment_id))

        if approve:
            cursor.execute("""
                SELECT total_amount
                FROM patient_bills
                WHERE bill_id = %s
                FOR UPDATE
            """, (payment["bill_id"],))

            bill = cursor.fetchone()

            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) AS paid
                FROM payment_records
                WHERE bill_id = %s
                  AND verification_status = 'Verified'
            """, (payment["bill_id"],))

            paid = Decimal(str(cursor.fetchone()["paid"]))
            total = Decimal(str(bill["total_amount"]))

            if paid >= total:
                bill_status = "Paid"
            elif paid > 0:
                bill_status = "Partially Paid"
            else:
                bill_status = "Pending"

            cursor.execute("""
                UPDATE patient_bills
                SET payment_status = %s
                WHERE bill_id = %s
            """, (bill_status, payment["bill_id"]))

        connection.commit()
        return True

    except Exception as error:
        connection.rollback()
        print("Payment Verification Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


def get_payment_receipt(payment_id):
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                pr.payment_id,
                pr.amount,
                pr.payment_method,
                pr.transaction_reference,
                pr.payment_date,
                pr.verification_status,
                b.invoice_number,
                b.total_amount,
                b.payment_status,
                p.patient_id,
                p.patient_name,
                u.name AS verified_by
            FROM payment_records pr
            JOIN patient_bills b ON b.bill_id = pr.bill_id
            JOIN patient_registration p
                ON p.patient_id = b.patient_id
            LEFT JOIN app_users u
                ON u.user_id = pr.verified_by
            WHERE pr.payment_id = %s
        """, (payment_id,))

        receipt = cursor.fetchone()

        if receipt and receipt["verification_status"] != "Verified":
            print("Receipt unavailable: payment is not verified.")
            return None

        return receipt

    except Exception as error:
        print("Receipt Retrieval Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


# ============================================================
# ADMIN PROFILE
# ============================================================

def get_admin_profile(user_id):
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, name, role, age, gender,
                   address, mobile_no, experience
            FROM app_users
            WHERE user_id = %s
        """, (user_id,))
        return cursor.fetchone()
    except Exception as error:
        print("Admin Profile Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


def update_admin_profile(user_id, name, mobile, address):
    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE app_users
            SET name = %s, mobile_no = %s, address = %s
            WHERE user_id = %s
        """, (name, mobile, address, user_id))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print("Profile Update Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


def change_user_password(user_id, old_password, new_password):
    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE app_users
            SET password = %s
            WHERE user_id = %s AND password = %s
        """, (new_password, user_id, old_password))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print("Password Update Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


# ============================================================
# STAFF MANAGEMENT
# ============================================================

def get_all_staff():
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, name, role, age, gender, address,
                   mobile_no, experience, employment_type,
                   specialty, joining_date, salary, account_status
            FROM app_users
            ORDER BY name
        """)
        return cursor.fetchall()
    except Exception as error:
        print("Staff Retrieval Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


def add_staff(data):
    """
    data order:
    name, password, role, age, gender, address, mobile,
    experience, employment_type, specialty, joining_date, salary
    """
    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        if len(data) != 12:
            raise ValueError("Staff data must contain 12 values.")

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO app_users (
                name, password, role, age, gender, address,
                mobile_no, experience, employment_type,
                specialty, joining_date, salary
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """, tuple(data))

        connection.commit()
        return cursor.lastrowid

    except Exception as error:
        connection.rollback()
        print("Staff Registration Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


def update_staff_status(user_id, status):
    if status not in ("Active", "Inactive"):
        return False

    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE app_users
            SET account_status = %s
            WHERE user_id = %s
        """, (status, user_id))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print("Staff Status Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


# ============================================================
# DUTY MANAGEMENT
# ============================================================

def add_duty(user_id, duty_date, shift, start_time,
             end_time, department, assigned_by):

    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        if shift not in ("Morning", "Evening", "Night"):
            raise ValueError("Invalid shift.")

        if start_time >= end_time:
            raise ValueError("End time must be later than start time.")

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id
            FROM app_users
            WHERE user_id = %s AND account_status = 'Active'
        """, (user_id,))

        if cursor.fetchone() is None:
            raise ValueError("Active staff member not found.")

        cursor.execute("""
            SELECT duty_id
            FROM duty_schedule
            WHERE user_id = %s
              AND duty_date = %s
              AND duty_status = 'Scheduled'
              AND start_time < %s
              AND end_time > %s
        """, (user_id, duty_date, end_time, start_time))

        if cursor.fetchone():
            raise ValueError("This staff member already has an overlapping duty.")

        cursor.execute("""
            INSERT INTO duty_schedule (
                user_id, duty_date, shift, start_time,
                end_time, department, assigned_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, duty_date, shift, start_time,
            end_time, department, assigned_by
        ))

        connection.commit()
        return cursor.lastrowid

    except Exception as error:
        connection.rollback()
        print("Duty Scheduling Error:", error)
        return False
    finally:
        _close_database(connection, cursor)


def get_duty_schedule(duty_date=None):
    connection = get_connector()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                ds.duty_id, ds.user_id, u.name, u.role,
                ds.duty_date, ds.shift, ds.start_time,
                ds.end_time, ds.department, ds.duty_status
            FROM duty_schedule ds
            JOIN app_users u ON u.user_id = ds.user_id
        """

        if duty_date:
            query += " WHERE ds.duty_date = %s"
            cursor.execute(query + " ORDER BY ds.start_time", (duty_date,))
        else:
            cursor.execute(query + """
                ORDER BY ds.duty_date DESC, ds.start_time
            """)

        return cursor.fetchall()

    except Exception as error:
        print("Duty Schedule Retrieval Error:", error)
        return None
    finally:
        _close_database(connection, cursor)


def update_duty_status(duty_id, status):
    if status not in ("Completed", "Cancelled"):
        return False

    connection = get_connector()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE duty_schedule
            SET duty_status = %s
            WHERE duty_id = %s AND duty_status = 'Scheduled'
        """, (status, duty_id))

        connection.commit()
        return cursor.rowcount > 0

    except Exception as error:
        connection.rollback()
        print("Duty Update Error:", error)
        return False
    finally:
        _close_database(connection, cursor)