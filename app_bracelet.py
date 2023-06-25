# Mini Project
import tkinter
import tkinter.messagebox
import tkinter.ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import folium
import pandas as pd
import webbrowser
from math import radians, sin, cos, sqrt, atan2
import tkinter as tk
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mysql.connector


class Database:
    def __init__(self):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ure363?!!?747",

        )

        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute("CREATE DATABASE IF NOT EXISTS final_project22")
        self.dbCursor.execute("USE final_project22")
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS doctor_table (id INT AUTO_INCREMENT PRIMARY KEY, "
                              "first_name VARCHAR(255), last_name VARCHAR(255), dob DATE, start_working_date DATE, "
                              "phone_number VARCHAR(15))")
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS patient_table (patient_id INT AUTO_INCREMENT PRIMARY KEY, "
                              "firstname VARCHAR(255), lastname VARCHAR(255), dateOfBirth DATE, gender VARCHAR(10), "
                              "address VARCHAR(255), contactNumber VARCHAR(15), emailAddress VARCHAR(255), "
                              "bloodType VARCHAR(10), history TEXT, doctor_id INT, "
                              "FOREIGN KEY (doctor_id) REFERENCES doctor_table(id))")
        self.dbCursor.execute(
            "CREATE TABLE IF NOT EXISTS measurement_table (patient_id INT,measurement_date_time DATETIME, "
            "heart_rate INT, spo2 INT, gps_lat FLOAT(10,6), gps_long FLOAT(10,6), "
            "PRIMARY KEY (measurement_date_time , patient_id), FOREIGN KEY (patient_id) REFERENCES patient_table(id))")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Insert(self, id,firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history,
               doctor_id):
        sql = "INSERT INTO patient_table (id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id,
            firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history,
            doctor_id
        )
        self.dbCursor.execute(sql, val)
        self.dbConnection.commit()

    def Insert_doctor(self, firstname, lastname, dateOfBirth, start_working_date, contactNumber):
        sql = "INSERT INTO doctor_table (firstname, lastname, dateOfBirth, start_working_date, contactNumbe) VALUES (%s, %s, %s, %s, %s)"
        val = (
            firstname, lastname, dateOfBirth, start_working_date, contactNumber)
        self.dbCursor.execute(sql, val)
        self.dbConnection.commit()

    def Update(self, id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType,
               history, doctor_id):
        sql = "UPDATE patient_table SET firstname = %s, lastname = %s, dateOfBirth = %s, gender = %s, address = %s, contactNumber = %s, emailAddress = %s, bloodType = %s, history = %s, doctor_id = %s WHERE id = %s"
        val = (
            firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id,
            id)
        self.dbCursor.execute(sql, val)
        self.dbConnection.commit()

    def Search(self, id):
        sql = "SELECT * FROM patient_table WHERE id = %s"
        val = (id,)
        self.dbCursor.execute(sql, val)
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def Search_doctor(self, id):
        sql = "SELECT * FROM doctor_table WHERE id = %s"
        val = (id,)
        self.dbCursor.execute(sql, val)
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def Delete(self, id):
        sql = "DELETE FROM patient_table WHERE id = %s"
        val = (id,)
        self.dbCursor.execute(sql, val)
        tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Patient data in the database")
        self.dbConnection.commit()

    def Delete_doctor(self, id):
        sql = "DELETE FROM doctor_table WHERE id = %s"
        val = (id,)
        self.dbCursor.execute(sql, val)
        tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Patient data in the database")
        self.dbConnection.commit()

    def Display(self):
        self.dbCursor.execute("SELECT * FROM patient_table")
        records = self.dbCursor.fetchall()
        return records

    def Display_doctor(self):
        self.dbCursor.execute("SELECT * FROM doctor_table")
        records = self.dbCursor.fetchall()
        return records


class Values:
    def Validate(self, firstname, lastname, contactNumber, emailAddress):
        if not (firstname.isalpha()):
            return "firstname"
        elif not (lastname.isalpha()):
            return "lastname"
        elif not (contactNumber.isdigit() and (len(contactNumber) == 10)):
            return "contactNumber"
        elif not (emailAddress.count("@") == 1 and emailAddress.count(".") > 0):
            return "emailAddress"
        else:
            return "SUCCESS"


class DoctorValues:
    def Validate(self, firstname, lastname, contactNumber):
        if not (firstname.isalpha()):
            return "firstname"
        elif not (lastname.isalpha()):
            return "lastname"
        elif not (contactNumber.isdigit() and (len(contactNumber) == 10)):
            return "contactNumber"
        else:
            return "SUCCESS"


class InsertWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Insert Patient Data ")
        bg_color = "Blue"
        fg_color = "white"

        self.id = tkinter.StringVar()
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.contactNumber = tkinter.StringVar()
        self.emailAddress = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor = tkinter.StringVar()

        self.genderType = ["Male", "Female", "Transgender", "Other"]
        self.bloodListType = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # Labels
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient Id", font=("times new roman", 10, "bold"),
                      width=25).grid(pady=5, column=1, row=1)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"), text="Date of Birth",
                      width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Gender", width=25).grid(pady=5, column=1, row=5)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Address", width=25).grid(pady=5, column=1, row=6)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Contact Number", width=25).grid(pady=5, column=1, row=7)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Email Address", width=25).grid(pady=5, column=1, row=8)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Blood Type", width=25).grid(pady=5, column=1, row=9)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="History of Patient", width=25).grid(pady=5, column=1, row=10)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Name of Doctor", width=25).grid(pady=5, column=1, row=11)

        self.idEntry = tkinter.Entry(self.window, width=25, textvariable=self.id)
        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.addressEntry = tkinter.Entry(self.window, width=25, textvariable=self.address)
        self.contactNumberEntry = tkinter.Entry(self.window, width=25, textvariable=self.contactNumber)
        self.emailAddressEntry = tkinter.Entry(self.window, width=25, textvariable=self.emailAddress)
        self.historyEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
        self.doctorEntry = tkinter.Entry(self.window, width=25, textvariable=self.doctor)

        self.idEntry.grid(pady=5, column=3, row=1)
        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.addressEntry.grid(pady=5, column=3, row=6)
        self.contactNumberEntry.grid(pady=5, column=3, row=7)
        self.emailAddressEntry.grid(pady=5, column=3, row=8)
        self.historyEntry.grid(pady=5, column=3, row=10)
        self.doctorEntry.grid(pady=5, column=3, row=11)
        self.dobEntry = DateEntry(self.window, date_pattern="yyyy-mm-dd")
        # Combobox widgets

        self.genderBox = tkinter.ttk.Combobox(self.window, values=self.genderType, width=25)
        self.bloodListBox = tkinter.ttk.Combobox(self.window, values=self.bloodListType, width=25)

        self.dobEntry.grid(pady=5, column=3, row=4)
        self.genderBox.grid(pady=5, column=3, row=5)
        self.bloodListBox.grid(pady=5, column=3, row=9)

        # Button widgets
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Insert", command=self.Insert).grid(pady=15, padx=5, column=1,
                                                                row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3,
                                                                       row=14)

        self.window.mainloop()

    def Insert(self):
        self.values = Values()
        self.database = Database()
        self.values = Values()
        self.database = Database()
        self.test = self.values.Validate(self.firstnameEntry.get(), self.lastnameEntry.get(),
                                         self.contactNumberEntry.get(), self.emailAddressEntry.get())
        # Rest of the code...
        if (self.test == "SUCCESS"):
            self.database.Insert(self.idEntry.get(), self.firstnameEntry.get(), self.lastnameEntry.get(),
                                 self.dobEntry.get(),
                                 self.genderBox.get(), self.addressEntry.get(),
                                 self.contactNumberEntry.get(), self.emailAddressEntry.get(), self.bloodListBox.get(),
                                 self.historyEntry.get(), self.doctorEntry.get())
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.contactNumberEntry.delete(0, tkinter.END)
        self.emailAddressEntry.delete(0, tkinter.END)
        self.bloodListBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)


class InsertDoctorWindow:
    def __init__(self):
        self.doctorvalue = DoctorValues()
        self.window = tkinter.Tk()
        self.window.wm_title("Insert Doctor Data ")
        bg_color = "Blue"
        fg_color = "white"

        # id, first_name, last_name, dob, start_working_date, phone_number
        self.id = tkinter.StringVar()
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.contactNumber = tkinter.StringVar()

        # Labels
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Doctor Id", font=("times new roman", 10, "bold"),
                      width=25).grid(pady=5, column=1, row=1)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Doctor First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Doctor Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"), text="Date of Birth",
                      width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="start work date", width=25).grid(pady=5, column=1, row=5)

        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Contact Number", width=25).grid(pady=5, column=1, row=9)

        self.idEntry = tkinter.Entry(self.window, width=25, textvariable=self.id)
        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.dobEntry = DateEntry(self.window, date_pattern="yyyy-mm-dd")
        self.StartWorkDateEntry = DateEntry(self.window, date_pattern="yyyy-mm-dd")
        self.contactNumberEntry = tkinter.Entry(self.window, width=25, textvariable=self.contactNumber)

        self.idEntry.grid(pady=5, column=3, row=1)
        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.dobEntry.grid(pady=5, column=3, row=4)
        self.StartWorkDateEntry.grid(pady=5, column=3, row=5)
        self.contactNumberEntry.grid(pady=5, column=3, row=6)


        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Insert", command=self.Insert).grid(pady=15, padx=5, column=1,
                                                                row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3,
                                                                       row=14)

        self.window.mainloop()

    def Insert(self):
        # self.values = Values()
        self.database = Database()
        self.test = self.doctorvalue.Validate(self.firstnameEntry.get(), self.lastnameEntry.get(),
                                              self.contactNumberEntry.get())
        if (self.test == "SUCCESS"):
            self.database.Insert_doctor(self.idEntry.get(), self.firstnameEntry.get(), self.lastnameEntry.get(),
                                        self.dobEntry.get(),
                                        self.contactNumberEntry.get())
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.contactNumberEntry.delete(0, tkinter.END)


class UpdateWindow:
    def __init__(self, id):
        self.window = tkinter.Tk()
        self.window.wm_title("Update data")
        bg_color = "Blue"
        fg_color = "white"

        # Initializing all the variables
        self.id = (id)
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.contactNumber = tkinter.StringVar()
        self.emailAddress = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor_id = tkinter.StringVar()

        self.genderType = ["Male", "Female", "Transgender", "Other"]
        self.bloodListType = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # Labels
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient Id", font=("times new roman", 10, "bold"),
                      width=25).grid(pady=5, column=1, row=1)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"), text="Date of Birth",
                      width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Gender", width=25).grid(pady=5, column=1, row=5)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Address", width=25).grid(pady=5, column=1, row=6)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Contact Number", width=25).grid(pady=5, column=1, row=7)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Email Address", width=25).grid(pady=5, column=1, row=8)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Blood Type", width=25).grid(pady=5, column=1, row=9)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="History of Patient", width=25).grid(pady=5, column=1, row=10)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Doctor id", width=25).grid(pady=5, column=1, row=11)

        # Set previous values
        self.database = Database()
        self.searchResults = self.database.Search(id)

        if len(self.searchResults) > 0:
            tkinter.Label(self.window, text=self.searchResults[0][1], width=25).grid(pady=5, column=2, row=2)
            tkinter.Label(self.window, text=self.searchResults[0][2], width=25).grid(pady=5, column=2, row=3)
            tkinter.Label(self.window, text=self.searchResults[0][3], width=25).grid(pady=5, column=2, row=4)
            tkinter.Label(self.window, text=self.searchResults[0][4], width=25).grid(pady=5, column=2, row=5)
            tkinter.Label(self.window, text=self.searchResults[0][5], width=25).grid(pady=5, column=2, row=6)
            tkinter.Label(self.window, text=self.searchResults[0][6], width=25).grid(pady=5, column=2, row=7)
            tkinter.Label(self.window, text=self.searchResults[0][7], width=25).grid(pady=5, column=2, row=8)
            tkinter.Label(self.window, text=self.searchResults[0][8], width=25).grid(pady=5, column=2, row=9)
            tkinter.Label(self.window, text=self.searchResults[0][9], width=25).grid(pady=5, column=2, row=10)
            tkinter.Label(self.window, text=self.searchResults[0][10], width=25).grid(pady=5, column=2, row=11)
            #tkinter.Label(self.window, text=self.searchResults[0][11], width=25).grid(pady=5, column=2, row=12)
        else:
            tkinter.messagebox.showinfo("Search Error", "No records found with the given ID")
        self.idEntry = tkinter.Entry(self.window, width=25, textvariable=self.id)
        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.addressEntry = tkinter.Entry(self.window, width=25, textvariable=self.address)
        self.contactNumberEntry = tkinter.Entry(self.window, width=25, textvariable=self.contactNumber)
        self.emailAddressEntry = tkinter.Entry(self.window, width=25, textvariable=self.emailAddress)
        self.historyEntry = tkinter.Entry(self.window, width=25, textvariable=self.history)
        self.doctorEntry = tkinter.Entry(self.window, width=25, textvariable=self.doctor_id)

        self.idEntry.grid(pady=5, column=3, row=1)
        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.addressEntry.grid(pady=5, column=3, row=8)
        self.contactNumberEntry.grid(pady=5, column=3, row=9)
        self.emailAddressEntry.grid(pady=5, column=3, row=10)
        self.historyEntry.grid(pady=5, column=3, row=12)
        self.doctorEntry.grid(pady=5, column=3, row=13)
        self.dobEntry = DateEntry(self.window, date_pattern="yyyy-mm-dd")

        # Combobox

        self.genderBox = tkinter.ttk.Combobox(self.window, values=self.genderType, width=20)
        self.bloodListBox = tkinter.ttk.Combobox(self.window, values=self.bloodListType, width=20)

        self.dobEntry.grid(pady=5, column=3, row=4)
        self.genderBox.grid(pady=5, column=3, row=7)
        self.bloodListBox.grid(pady=5, column=3, row=11)

        # Button
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Update", command=self.Update).grid(pady=15, padx=5, column=1,
                                                                row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3,
                                                                       row=14)

        self.window.mainloop()

    def Update(self):
        self.database = Database()
        self.database.Update(self.firstnameEntry.get(), self.lastnameEntry.get(), self.dobEntry.get(),
                             self.genderBox.get(), self.addressEntry.get(),
                             self.contactNumberEntry.get(),
                             self.emailAddressEntry.get(), self.bloodListBox.get(), self.historyEntry.get(),
                             self.doctorEntry.get(), self.id)
        tkinter.messagebox.showinfo("Updated data", "Successfully updated the above data in the database")

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.contactNumberEntry.delete(0, tkinter.END)
        self.emailAddressEntry.delete(0, tkinter.END)
        self.bloodListBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)


class DatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("Database View")

        # Label widgets
        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = (
            "id", "firstname", "lastname", "dateOfBirth", "gender", "address",
            "contactNumber", "emailAddress", "bloodType", "history",
            "doctor_id")

        # id, firstname, lastname, dateOfBirth, gender, address, contactNumber, emailAddress, bloodType, history, doctor_id
        # Treeview column headings
        self.databaseView.heading("id", text="Patient ID")
        self.databaseView.heading("firstname", text="First Name")
        self.databaseView.heading("lastname", text="Last Name")
        self.databaseView.heading("dateOfBirth", text="Date of Birth")
        self.databaseView.heading("gender", text="Gender")
        self.databaseView.heading("address", text="Home Address")
        self.databaseView.heading("contactNumber", text="Contact Number")
        self.databaseView.heading("emailAddress", text="Email Address")
        self.databaseView.heading("bloodType", text="Blood Type")
        self.databaseView.heading("history", text="History")
        self.databaseView.heading("doctor_id", text="Doctor")

        # Treeview columns
        self.databaseView.column("id", width=100)
        self.databaseView.column("firstname", width=100)
        self.databaseView.column("lastname", width=100)
        self.databaseView.column("dateOfBirth", width=100)
        self.databaseView.column("gender", width=100)
        self.databaseView.column("address", width=200)
        self.databaseView.column("contactNumber", width=100)
        self.databaseView.column("emailAddress", width=200)
        self.databaseView.column("bloodType", width=100)
        self.databaseView.column("history", width=100)
        self.databaseView.column("doctor_id", width=100)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ure363?!!?747",
            database="final_project22"
        )
        self.cursor = self.db.cursor()

        # Insert data into MySQL database table
        self.cursor.execute("SELECT * FROM patient_table")
        data = self.cursor.fetchall()

        for record in data:
            self.databaseView.insert('', 'end', values=record)

        self.databaseViewWindow.mainloop()


class DoctorDatabaseView:
    def __init__(self, data):
        self.doctordatabaseViewWindow = tkinter.Tk()
        self.doctordatabaseViewWindow.wm_title("Database View")

        # Label widgets
        tkinter.Label(self.doctordatabaseViewWindow, text="Doctors View Window", width=25).grid(pady=5, column=1, row=1)

        self.doctordatabaseView = tkinter.ttk.Treeview(self.doctordatabaseViewWindow)
        self.doctordatabaseView.grid(pady=5, column=1, row=2)
        self.doctordatabaseView["show"] = "headings"
        self.doctordatabaseView["columns"] = (
            "id", "firstname", "lastname", "dob", "start_working_date", "phone_number")

        # Treeview column headings
        self.doctordatabaseView.heading("id", text="Doctor ID")
        self.doctordatabaseView.heading("firstname", text="First Name")
        self.doctordatabaseView.heading("lastname", text="Last Name")
        self.doctordatabaseView.heading("dob", text="Date of Birth")
        self.doctordatabaseView.heading("start_working_date", text="Start work date")
        self.doctordatabaseView.heading("phone_number", text="Phone Number")

        # id,first_name, last_name ,dob,start_working_date,phone_number
        # Treeview columns
        self.doctordatabaseView.column("id", width=100)
        self.doctordatabaseView.column("firstname", width=100)
        self.doctordatabaseView.column("lastname", width=100)
        self.doctordatabaseView.column("dob", width=100)
        self.doctordatabaseView.column("start_working_date", width=100)
        self.doctordatabaseView.column("phone_number", width=100)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ure363?!!?747",
            database="final_project22"
        )
        self.cursor = self.db.cursor()

        # Insert data into MySQL database table
        self.cursor.execute("SELECT * FROM doctor_table")
        data = self.cursor.fetchall()

        for record in data:
            self.doctordatabaseView.insert('', 'end', values=record)

        self.doctordatabaseViewWindow.mainloop()


class patientAdminstrationWindow:
    def __init__(self):
        self.patientWindow = tkinter.Tk()
        self.patientWindow.wm_title("Patient Administration")
        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'green'
        tkinter.Label(self.patientWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Patient Administration",
                      font=("times new roman", 20, "bold"), width=60).grid(pady=20, column=1, row=1)

        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Insert new patient", font=("times new roman", 15, "bold"), command=self.Insert).grid(
            pady=15,
            column=1,
            row=3)
        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Update patient", font=("times new roman", 15, "bold"), command=self.Update).grid(pady=15,
                                                                                                              column=1,
                                                                                                              row=4)
        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Search patient", font=("times new roman", 15, "bold"), command=self.Search).grid(pady=15,
                                                                                                              column=1,
                                                                                                              row=5)
        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Delete patient", font=("times new roman", 15, "bold"), command=self.Delete).grid(pady=15,
                                                                                                              column=1,
                                                                                                              row=6)
        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Display patient", font=("times new roman", 15, "bold"), command=self.Display).grid(pady=15,
                                                                                                                column=1,
                                                                                                                row=7)
        tkinter.Button(self.patientWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Exit",
                       font=("times new roman", 15, "bold"), command=self.patientWindow.destroy).grid(pady=15,
                                                                                                      column=1,
                                                                                                      row=8)

        self.patientWindow.mainloop()

    def Insert(self):
        self.insertWindow = InsertWindow()

    def Update(self):
        self.updateIDWindow = tkinter.Tk()
        self.updateIDWindow.wm_title("Update data")

        # Initializing all the variables
        self.id = tkinter.StringVar()

        # Label
        tkinter.Label(self.updateIDWindow, text="Enter the ID to update", width=50).grid(pady=20, row=1)

        # Entry widgets
        self.idEntry = tkinter.Entry(self.updateIDWindow, width=5, textvariable=self.id)

        self.idEntry.grid(pady=10, row=2)

        # Button widgets
        tkinter.Button(self.updateIDWindow, width=20, text="Update", command=self.updateID).grid(pady=10, row=3)

        self.updateIDWindow.mainloop()

    def updateID(self):
        self.updateWindow = UpdateWindow(self.idEntry.get())
        self.updateIDWindow.destroy()

    def Search(self):
        self.searchWindow = SearchDeleteWindow("Search")

    def Delete(self):
        self.deleteWindow = SearchDeleteWindow("Delete")

    def Display(self):
        self.database = Database()
        self.data = self.database.Display()
        self.displayWindow = DatabaseView(self.data)


class DoctorAdminstrationWindow:
    def __init__(self):
        self.doctorWindow = tkinter.Tk()
        self.doctorWindow.wm_title("Doctor Administration")
        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'green'
        tkinter.Label(self.doctorWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Doctor Administration",
                      font=("times new roman", 20, "bold"), width=60).grid(pady=20, column=1, row=1)

        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Insert new doctor", font=("times new roman", 15, "bold"), command=self.Insert_doctor).grid(
            pady=15,
            column=1,
            row=3)
        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Update doctor", font=("times new roman", 15, "bold"), command=self.Update).grid(pady=15,
                                                                                                             column=1,
                                                                                                             row=4)
        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Search doctor", font=("times new roman", 15, "bold"), command=self.Search_doctor).grid(
            pady=15,
            column=1,
            row=5)
        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Delete doctor", font=("times new roman", 15, "bold"), command=self.Delete_doctor).grid(
            pady=15,
            column=1,
            row=6)
        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Display doctor", font=("times new roman", 15, "bold"), command=self.Display_doctor).grid(
            pady=15,
            column=1,
            row=7)
        tkinter.Button(self.doctorWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Exit",
                       font=("times new roman", 15, "bold"), command=self.doctorWindow.destroy).grid(pady=15,
                                                                                                     column=1,
                                                                                                     row=8)

        self.doctorWindow.mainloop()

    def Insert_doctor(self):
        self.insertWindow = InsertDoctorWindow()

    def Update(self):
        self.updateIDWindow = tkinter.Tk()
        self.updateIDWindow.wm_title("Update data")

        # Initializing all the variables
        self.id = tkinter.StringVar()

        # Label
        tkinter.Label(self.updateIDWindow, text="Enter the ID to update", width=50).grid(pady=20, row=1)

        # Entry widgets
        self.idEntry = tkinter.Entry(self.updateIDWindow, width=5, textvariable=self.id)

        self.idEntry.grid(pady=10, row=2)

        # Button widgets
        tkinter.Button(self.updateIDWindow, width=20, text="Update", command=self.updateID).grid(pady=10, row=3)

        self.updateIDWindow.mainloop()

    def updateID(self):
        self.updateWindow = UpdateWindow(self.idEntry.get())
        self.updateIDWindow.destroy()

    def Search_doctor(self):
        self.searchWindow = SearchDeletedoctorWindow("Search")

    def Delete_doctor(self):
        self.deleteWindow = SearchDeletedoctorWindow("Delete")

    def Display_doctor(self):
        self.database = Database()
        self.data = self.database.Display_doctor()
        self.displayWindow = DoctorDatabaseView(self.data)


class measuresWindow(Database):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.measuresWindow = tkinter.Tk()
        self.measuresWindow.wm_title("Patient Measurements")
        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'green'
        tkinter.Label(self.measuresWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Measurements Page",
                      font=("times new roman", 20, "bold"), width=60).grid(pady=20, column=1, row=1)

        tkinter.Button(self.measuresWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Take Measurements", font=("times new roman", 15, "bold"),
                       command=self.take_measurements).grid(
            pady=15, column=1, row=3)
        tkinter.Button(self.measuresWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Search Patient Measurements", font=("times new roman", 15, "bold"),
                       command=self.search_measurements).grid(pady=15,
                                                              column=1,
                                                              row=4)
        tkinter.Button(self.measuresWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Display Measurements", font=("times new roman", 15, "bold"),
                       command=self.display_measurements).grid(pady=15,
                                                               column=1,
                                                               row=5)
        tkinter.Button(self.measuresWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Exit", font=("times new roman", 15, "bold"), command=self.measuresWindow.destroy).grid(
            pady=15,
            column=1,
            row=6)

        self.measuresWindow.mainloop()

    def take_measurements(self):
        # Prompt for patient ID
        # ... implementation of taking measurements ...
        pass

    def search_measurements(self):
        # Add functionality for searching patient measurements here
        pass

    def display_measurements(self):
        display_window = tkinter.Toplevel(self.measuresWindow)
        display_window.title("Display Measurements")
        display_window.geometry("400x200")


        def show_spo2_heartrate():
            patient_id = patient_id_entry.get()
            query = f"SELECT * FROM measurement_table WHERE patient_id = {patient_id}"
            self.dbCursor.execute(query)
            rows = self.dbCursor.fetchall()
            # Convert rows to a DataFrame
            rows_df = pd.DataFrame(rows,
                                   columns=['patient_id', 'measurement_date_time', 'heart_rate', 'spo2', 'gps_lat',
                                            'gps_long'])

            # Access columns using column names
            heart_rate_values = rows_df['heart_rate']
            spo2_values = rows_df['spo2']
            timestamps = pd.to_datetime(rows_df['measurement_date_time'], format='%Y-%m-%d %H:%M:%S')



            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
            ax1.plot(timestamps, heart_rate_values, 'b.-')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Heart Rate')

            ax2.plot(timestamps, spo2_values, 'r.-')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('SpO2')

            # Format the date and time
            date_fmt = '%Y-%m-%d\n'
            time_fmt = '%H:%M:%S'

            ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt + time_fmt))

            ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax2.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt + time_fmt))

            plt.tight_layout()
            plt.show(block=False)

            max_heart_rate_avg = 0
            min_spo2_avg = 0
            for i in range(len(rows)):
                if i >= 4:
                    heart_rate_avg = sum(heart_rate_values[i - 4:i + 1]) / 5
                    spo2_avg = sum(spo2_values[i - 4:i + 1]) / 5
                    if heart_rate_avg > 90 and heart_rate_avg > max_heart_rate_avg:
                        max_heart_rate_avg = heart_rate_avg
                    if spo2_avg < 90 and spo2_avg > min_spo2_avg:
                        min_spo2_avg = spo2_avg
            warnings = []
            if max_heart_rate_avg > 0:
                warnings.append(f"Patient heart rate is high! Maximum average: {max_heart_rate_avg:.2f}")
            if min_spo2_avg > 0:
                warnings.append(f"Patient SpO2 is low! Maximum average: {min_spo2_avg:.2f}")

            root = tk.Tk()
            root.withdraw()

            def show_warnings():
                if warnings:
                    messagebox.showwarning("Warnings", "\n".join(warnings))

            root.after(200, show_warnings)
            root.mainloop()

            def show_warnings():
                if warnings:
                    messagebox.showwarning("Warnings", "\n".join(warnings))

            root.after(200, show_warnings)
            root.mainloop()

        def generate_patient_map():
            map_center = [32.08063, 34.78857]
            m = folium.Map(location=map_center, zoom_start=12)
            patient_id = patient_id_entry.get()
            query = f"SELECT * FROM measurement_table WHERE patient_id = {patient_id}"
            self.dbCursor.execute(query)
            rows = self.dbCursor.fetchall()
            rows_df = pd.DataFrame(rows,
                                   columns=['patient_id', 'measurement_date_time', 'heart_rate', 'spo2', 'gps_lat',
                                            'gps_long'])

            def add_patient_markers(rows_df):
                grouped_df = rows_df.groupby(['gps_lat', 'gps_long'])

                for (lat, lon), group in grouped_df:
                    for index, row in group.iterrows():
                        timestamp = row['measurement_date_time']
                        popup_text = f"Timestamp: {timestamp}"
                        folium.Marker(
                            location=[lat, lon],
                            icon=folium.DivIcon(
                                icon_size=(30, 30),
                                icon_anchor=(15, 15),
                                html='<div><img src="patient_icon.png" style="width:30px;height:30px;"></div>'
                            ),
                            popup=popup_text
                        ).add_to(m)

            def calculate_distance(lat1, lon1, lat2, lon2):
                # approximate radius of Earth in km
                R = 6371.0

                lat1_rad = radians(lat1)
                lon1_rad = radians(lon1)
                lat2_rad = radians(lat2)
                lon2_rad = radians(lon2)

                dlon = lon2_rad - lon1_rad
                dlat = lat2_rad - lat1_rad

                a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                distance = R * c
                return distance

            def check_patient_activity(rows):
                max_distance = 0
                for i in range(1, len(rows)):
                    lat1, lon1 = rows.loc[i - 1, 'gps_lat'], rows.loc[i - 1, 'gps_long']
                    lat2, lon2 = rows.loc[i, 'gps_lat'], rows.loc[i, 'gps_long']
                    distance = calculate_distance(lat1, lon1, lat2, lon2)
                    if distance > max_distance:
                        max_distance = distance

                if max_distance > 10:
                    warning_text = f"Patient is running away! Maximum distance from Ichilov: {round(max_distance)} km"
                    messagebox.showwarning("Warning", warning_text)
                    warning_label = tk.Label(window, text=warning_text)
                    warning_label.pack()

            if len(rows_df) > 0:
                # Add patient markers to the map
                add_patient_markers(rows_df)

                # Create a path connecting the measurements
                patient_measurements = rows_df[['gps_lat', 'gps_long']].values.tolist()
                folium.PolyLine(locations=patient_measurements, color='red', weight=3).add_to(m)

                # Save the map to an HTML file
                map_html = 'patient_map.html'
                m.save(map_html)

                # Create a Tkinter window
                window = tk.Tk()
                window.title("Patient Map and Warnings")

                # Open the HTML file in the default web browser
                webbrowser.open(map_html)

                # Check patient activity and show warnings
                check_patient_activity(rows_df)

            else:
                messagebox.showwarning("Warning", "No measurements found for the specified patient.")

            window.mainloop()

        def show_patient_location():
            # Add functionality to show patient location on the map here
            generate_patient_map()

        patient_id_label = tkinter.Label(display_window, text="Patient ID:")
        patient_id_label.pack()

        patient_id_entry = tkinter.Entry(display_window)
        patient_id_entry.pack()

        # Create buttons for showing heart rate and spo2 graph, and patient location
        spo2_heartrate_button = tkinter.Button(display_window, width=30, relief=tkinter.GROOVE, fg='white', bg='blue',
                                               text="Show Heart Rate and SpO2 Graph",
                                               font=("times new roman", 12, "bold"),
                                               command=lambda: show_spo2_heartrate())
        spo2_heartrate_button.pack(pady=20)

        patient_location_button = tkinter.Button(display_window, width=30, relief=tkinter.GROOVE, fg='white', bg='blue',
                                                 text="Show Patient Location", font=("times new roman", 12, "bold"),
                                                 command=show_patient_location)
        patient_location_button.pack(pady=20)




class SearchDeleteWindow:
    def __init__(self, task):
        window = tkinter.Tk()
        window.wm_title(task + " data")

        # Initializing all the variables
        self.id = tkinter.StringVar()
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.heading = "Please enter Patient ID to " + task

        # Labels
        tkinter.Label(window, text=self.heading, width=50).grid(pady=20, row=1)
        tkinter.Label(window, text="Patient ID", width=10).grid(pady=5, row=2)

        # Entry widgets
        self.idEntry = tkinter.Entry(window, width=5, textvariable=self.id)

        self.idEntry.grid(pady=5, row=3)

        # Button widgets
        if (task == "Search"):
            tkinter.Button(window, width=20, text=task, command=self.Search).grid(pady=15, padx=5, column=1, row=14)
        elif (task == "Delete"):
            tkinter.Button(window, width=20, text=task, command=self.Delete).grid(pady=15, padx=5, column=1, row=14)

    def Search(self):
        self.database = Database()
        self.data = self.database.Search(self.idEntry.get())
        self.databaseView = DatabaseView(self.data)

    def Delete(self):
        self.database = Database()
        self.database.Delete(self.idEntry.get())


class SearchDeletedoctorWindow:
    def __init__(self, task):
        window = tkinter.Tk()
        window.wm_title(task + " data")

        # Initializing all the variables
        self.id = tkinter.StringVar()
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.heading = "Please enter Doctor ID to " + task

        # Labels
        tkinter.Label(window, text=self.heading, width=50).grid(pady=20, row=1)
        tkinter.Label(window, text="Doctor ID", width=10).grid(pady=5, row=2)

        # Entry widgets
        self.idEntry = tkinter.Entry(window, width=5, textvariable=self.id)

        self.idEntry.grid(pady=5, row=3)

        # Button widgets
        if (task == "Search"):
            tkinter.Button(window, width=20, text=task, command=self.Search).grid(pady=15, padx=5, column=1, row=14)
        elif (task == "Delete"):
            tkinter.Button(window, width=20, text=task, command=self.Delete).grid(pady=15, padx=5, column=1, row=14)

    def Search(self):
        self.database = Database()
        self.data = self.database.Search_doctor(self.idEntry.get())
        self.databaseView = DatabaseView(self.data)

    def Delete(self):
        self.database = Database()
        self.database.Delete_doctor(self.idEntry.get())


class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("bracelet Information system Home Page")
        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'green'
        tkinter.Label(self.homePageWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Home Page",
                      font=("times new roman", 20, "bold"), width=60, height=6).grid(pady=20, column=1, row=1)

        # tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Insert",
        #               font=("times new roman", 15, "bold"), command=self.Insert).grid(pady=15, column=1, row=3)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="patient administration",
                       font=("times new roman", 15, "bold"), command=self.patient_admin).grid(pady=15, column=1, row=3)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="measurements",
                       font=("times new roman", 15, "bold"), command=self.measure).grid(pady=15, column=1, row=4)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="doctor administration",
                       font=("times new roman", 15, "bold"), command=self.doctor_admin).grid(pady=15, column=1, row=5)
        """tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Update",
                       font=("times new roman", 15, "bold"), command=self.Update).grid(pady=15, column=1, row=7)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Search",
                       font=("times new roman", 15, "bold"), command=self.Search).grid(pady=15, column=1, row=8)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Delete",
                       font=("times new roman", 15, "bold"), command=self.Delete).grid(pady=15, column=1, row=9)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Display",
                       font=("times new roman", 15, "bold"), command=self.Display).grid(pady=15, column=1,
                                                                                        row=10)
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                       text="Patient measurments",
                       font=("times new roman", 15, "bold"), command=self.measure).grid(pady=15, column=1, row=11)"""
        tkinter.Button(self.homePageWindow, width=30, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Exit",
                       font=("times new roman", 15, "bold"), command=self.homePageWindow.destroy).grid(pady=15,
                                                                                                       column=1,
                                                                                                       row=6)

        self.homePageWindow.mainloop()

    def Insert(self):
        self.insertWindow = InsertWindow()

    def measure(self):
        self.measuresWindow = measuresWindow()

    def patient_admin(self):
        self.patientAdminstrationWindow = patientAdminstrationWindow()

    def doctor_admin(self):
        self.DoctorAdminstrationWindow = DoctorAdminstrationWindow()

    def Update(self):
        self.updateIDWindow = tkinter.Tk()
        self.updateIDWindow.wm_title("Update data")

        # Initializing all the variables
        self.id = tkinter.StringVar()

        # Label
        tkinter.Label(self.updateIDWindow, text="Enter the ID to update", width=50).grid(pady=20, row=1)

        # Entry widgets
        self.idEntry = tkinter.Entry(self.updateIDWindow, width=5, textvariable=self.id)

        self.idEntry.grid(pady=10, row=2)

        # Button widgets
        tkinter.Button(self.updateIDWindow, width=20, text="Update", command=self.updateID).grid(pady=10, row=3)

        self.updateIDWindow.mainloop()

    def updateID(self):
        self.updateWindow = UpdateWindow(self.idEntry.get())
        self.updateIDWindow.destroy()

    def Search(self):
        self.searchWindow = SearchDeleteWindow("Search")

    def Delete(self):
        self.deleteWindow = SearchDeleteWindow("Delete")

    def Display(self):
        self.database = Database()
        self.data = self.database.Display()
        self.displayWindow = DatabaseView(self.data)


homePage = HomePage()
