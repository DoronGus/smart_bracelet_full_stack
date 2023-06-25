import pandas as pd
import mysql.connector

host = "localhost"
user = "root"
password = "ure363?!!?747"

# Connect to the MySQL database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database="final_project22"
)
"""excel_file = "patient_table.csv"
df = pd.read_csv(excel_file)
# df['measurement_date_time'] = pd.to_datetime(df['measurement_date_time'])
# df['measurement_date_time'] = df['measurement_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Insert data into the measurement_table
cursor = connection.cursor()
for _, row in df.iterrows():
    insert_query = "INSERT INTO patient_table (id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        row['id'], row['firstname'], row['lastname'], row['dateOfBirth'], row['gender'], row['address'],
        row['contactNumber'], row['emailAddress'], row['bloodType'], row['history'], row['doctor_id'])
    cursor.execute(insert_query, values)

connection.commit()
cursor.close()
connection.close()
# Read the Excel file
"""
"""
excel_file = "doctor_table.csv"
df = pd.read_csv(excel_file)
# df['measurement_date_time'] = pd.to_datetime(df['measurement_date_time'])
# df['measurement_date_time'] = df['measurement_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Insert data into the measurement_table
cursor = connection.cursor()
for _, row in df.iterrows():
    insert_query = "INSERT INTO doctor_table (id,first_name,last_name,dob,start_working_date,phone_number) VALUES (%s, %s, %s, %s, %s,%s)"
    values = (
        row['id'], row['first_name'], row['last_name'], row['dob'], row['start_working_date'], row['phone_number'])
    cursor.execute(insert_query, values)

connection.commit()
cursor.close()
connection.close()
"""
excel_file = "measurments.csv"
df = pd.read_csv(excel_file)
df['measurement_date_time'] = pd.to_datetime(df['measurement_date_time'])
df['measurement_date_time'] = df['measurement_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Insert data into the measurement_table
cursor = connection.cursor()
for _, row in df.iterrows():
    insert_query = "INSERT INTO measurement_table (patient_id, measurement_date_time, heart_rate, spo2,gps_lat,gps_long) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (
    row['patient_id'], row['measurement_date_time'], row['heart_rate'], row['spo2'], row['gps_lat'], row['gps_long'])
    cursor.execute(insert_query, values)
connection.commit()
cursor.close()
connection.close()
"""
# Read the Excel file
excel_file = "patient_table.csv"
df = pd.read_csv(excel_file)
# df['measurement_date_time'] = pd.to_datetime(df['measurement_date_time'])
# df['measurement_date_time'] = df['measurement_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Insert data into the measurement_table
cursor = connection.cursor()
for _, row in df.iterrows():
    insert_query = "INSERT INTO patient_table (id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        row['id'], row['firstname'], row['lastname'], row['dateOfBirth'], row['gender'], row['address'],
        row['contactNumber'], row['emailAddress'], row['bloodType'], row['history'], row['doctor_id'])
    cursor.execute(insert_query, values)

connection.commit()
cursor.close()
connection.close()
"""
