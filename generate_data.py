"""
import csv
import random
import datetime
def generate_patient_table():
    # Generate random Israeli first names and last names
    first_names = ["Avraham", "Yael", "Daniel", "Noa", "Itay", "Tamar", "Eitan", "Maya", "Yosef", "Shira"]
    last_names = ["Levi", "Cohen", "Mizrachi", "Katz", "Azoulay", "Peretz", "Ohana", "Barak", "Shapira", "Avrahami"]

    # Generate random contact numbers
    contact_prefixes = ["050", "052", "053", "054"]
    contact_numbers = [str(random.randint(1000000, 9999999)) for _ in range(10)]

    # Generate random patient data
    patients = []
    for patient_id in patient_ids:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        date_of_birth = random_date()
        gender = random.choice(["Male", "Female"])
        address = "Sample Address"
        contact_number = random.choice(contact_prefixes) + random.choice(contact_numbers)
        email_address = f"{first_name.lower()}.{last_name.lower()}@example.com"
        blood_type = random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        history = random.choice(["Allergy", "Chronic Illness"])
        doctor_id = random.choice(["201223267", "344234567", "301984567"])

        patient = (patient_id, first_name, last_name, date_of_birth, gender, address, contact_number,
                   email_address, blood_type, history, doctor_id)
        patients.append(patient)
    #id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id
    # Write patient data to CSV file
    with open('patient_table.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "firstname", "lastname", "dateOfBirth", "gender", "address",
                         "contactNumber", "emailAddress", "bloodType", "history", "doctor_id"])
        writer.writerows(patients)

    print("Patient table successfully generated.")

def random_date():
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2000, 12, 31)
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    return start_date + datetime.timedelta(days=random_days)

# Specify the patient IDs
patient_ids = [
    "201234567", "301234567", "401234567",
    "201234568", "301234568", "401234568",
    "201234569", "301234569", "401234569",
    "201234570", "301234570", "401234570",
    "201234571", "301234571", "401234571",
    "201234572", "301234572", "401234572"
]

# Generate patient table
generate_patient_table()
"""
import csv
import datetime
import random

def generate_doctor_table():
    # Generate random Israeli first names and last names
    first_names = ["Avraham", "Yael", "Daniel", "Noa", "Itay", "Tamar", "Eitan", "Maya", "Yosef", "Shira"]
    last_names = ["Levi", "Cohen", "Mizrachi", "Katz", "Azoulay", "Peretz", "Ohana", "Barak", "Shapira", "Avrahami"]

    # Generate random doctor data
    doctors = []
    for doctor_id in doctor_ids:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        dob = random_date()
        start_working_date = dob + datetime.timedelta(days=26*365)
        phone_number = f"050-{random.randint(1000000, 9999999)}"

        doctor = (doctor_id, first_name, last_name, dob, start_working_date, phone_number)
        doctors.append(doctor)

    # Write doctor data to CSV file
    with open('doctor_table.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "first_name", "last_name", "dob", "start_working_date", "phone_number"])
        writer.writerows(doctors)

    print("Doctor table successfully generated.")

def random_date():
    start_date = datetime.date(1960, 1, 1)
    end_date = datetime.date(1997, 12, 31)
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    return start_date + datetime.timedelta(days=random_days)

# Specify the doctor IDs
doctor_ids = ["201223267", "344234567", "301984567"]

# Generate doctor table
generate_doctor_table()