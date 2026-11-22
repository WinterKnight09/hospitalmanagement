from decimal import Decimal
from database.dbconnector import get_connector


def get_patient_for_billing(patient_id):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                PATIENT_ID,
                PATIENT_NAME,
                MOBILE_NUMBER,
                PATIENT_TYPE
            FROM PATIENT_REGISTRATION
            WHERE PATIENT_ID = %s
        """, (patient_id,))

        return cursor.fetchone()

    except Exception as error:
        print("Patient Lookup Error:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def save_bill(patient_id, consultation, medicine, tests, user_id):

    connection = get_connector()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = None

    try:
        consultation = Decimal(str(consultation))
        medicine = Decimal(str(medicine))
        tests = Decimal(str(tests))

        total = consultation + medicine + tests

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO PATIENT_BILLS (
                PATIENT_ID,
                CONSULTATION_FEE,
                MEDICINE_CHARGES,
                TEST_CHARGES,
                TOTAL_AMOUNT,
                CREATED_BY
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
            UPDATE PATIENT_BILLS
            SET INVOICE_NUMBER = %s
            WHERE BILL_ID = %s
        """, (invoice_number, bill_id))

        connection.commit()

        return {
            "bill_id": bill_id,
            "invoice_number": invoice_number,
            "total": total
        }

    except Exception as error:
        connection.rollback()
        print("Bill Save Error:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_bill_by_id(bill_id):

    connection = get_connector()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                b.*,
                p.PATIENT_NAME,
                p.MOBILE_NUMBER,
                u.name AS GENERATED_BY
            FROM PATIENT_BILLS b
            JOIN PATIENT_REGISTRATION p
                ON b.PATIENT_ID = p.PATIENT_ID
            LEFT JOIN app_users u
                ON b.CREATED_BY = u.user_id
            WHERE b.BILL_ID = %s
        """, (bill_id,))

        return cursor.fetchone()

    except Exception as error:
        print("Bill Retrieval Error:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()
