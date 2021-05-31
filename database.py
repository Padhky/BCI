import mysql.connector as sql_con
import pandas as pd
from tabulate import tabulate

# Without doing the work multiple times, please look at:
# https://www.w3schools.com/python/python_mysql_getstarted.asp
# This gives a good overview of how we access MySQL functionality from Python

database = sql_con.connect(
    # since host is local and the application has root access
    host="localhost",
    user="root",
    passwd="tOWtTKCC3wCkii9CuLGT",
    # needed for acceptation of the password
    auth_plugin="mysql_native_password",
    # After database was created you can directly connect to it
    database="eeg",
)
# COMMAND to create database in mysql
# sql_cursor.execute("CREATE DATABASE EEG_Data")

# COMMAND to delete a database
# sql_cursor.execute("DROP DATABASE EEGdata")

# cursor for database and keeping database up to date
sql_cursor = database.cursor()

# COMMAND to show existing databases
sql_cursor.execute("SHOW DATABASES")
for datba in sql_cursor:
    print(datba)


try:
    sql = "CREATE TABLE IF NOT EXISTS Files " \
            "(prof_name VARCHAR(255), prof_key INT, " \
            "file_name VARCHAR(255), " \
            "file_path VARCHAR(255), " \
            "file_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"
    sql_cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS Profiles (prof_name VARCHAR(255), id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"

    sql_cursor.execute(sql)
    print("Successfully created tables: Files and Profiles\n")
except Exception as E1:
    print("Exception happened\n")


class NonExistent(Exception):
    print("Mentioned element is not found:\n")

# Visual representation of a table for the backend
# Since tables are varying in size, each table may need a specific formation
# what can be defined below
def print_table(elements, source):
    sql = "SELECT"
    counter = 1
    for i in elements:
        if counter != len(elements):
            sql += " " + i + ","
            counter += 1
        else:
            sql += " " + i + " "
    sql += "FROM " + source
    print("Command inserted for selection: " + str(sql) + "\n")

    if source == "Profiles":
        try:
            sql_cursor.execute(sql)
            res = sql_cursor.fetchall()
            print(tabulate(res, headers=["Profile Name", "ID"], tablefmt="psql"))
        except Exception as PRINT_ERROR:
            print("Please check your input to the function.\nInput needs to be tuple or list of existing elements" +
                  " Error: \n" + str(PRINT_ERROR))

    elif source == "Files":
        try:
            sql_cursor.execute(sql)
            res = sql_cursor.fetchall()
            print(tabulate(res, headers=["Profile Name", "Profile ID", "File Name", "Path", "File ID"], tablefmt="psql"))
        except Exception as PRINT_ERROR:
            print("Please check your input to the function.\nInput needs to be tuple or list of existing elements" +
                  " Error: \n" + str(PRINT_ERROR))
    else:
        print("No existing mode chosen")


def show_entries(table):
    try:
        sql = "SELECT * FROM " + str(table)
        sql_cursor.execute(sql)
        names = sql_cursor.fetchall()
        print(names)
        res = []

        if len(names) == 0:
            res = ['Empty']

        elif table == "Profiles":
            for elem in names:
                res.append(elem[0])

        elif table == "Files":
            for elem in names:
                res.append(elem)

        return res

    except:
        print("Entries couldn't be shown")


# Uncomment when something went wrong and enter name of table
# sql_cursor.execute("DROP TABLE *Table name*")


# Showing all tables in database
print("Tables currently in " + str(database.database) + "\n")
sql_cursor.execute("SHOW TABLES")
for tab in sql_cursor:
    print(str(tab) + "\n")

# The following functions are access from the GUI, so we can interact with the database
# from the GUI

def delete_profile_from_db(name):
    try:
        sql = "SELECT COUNT(1) FROM Profiles WHERE prof_name = \'" + str(name) + "\'"
        sql_cursor.execute(sql)
        if sql_cursor.fetchone()[0]:
            print("Name can be deleted")
        else:
            raise NonExistent

    except NonExistent:
        print(str(name) + " could not been deleted.\n" + "Please check for typos\n")

    try:
        sql = "DELETE FROM Profiles prof_name WHERE prof_name = \'" + str(name) +"\'"
        print(sql)
        sql_cursor.execute(sql)
        database.commit()

    except Exception as DE:
        print("Error while deleting profile record from database\n\n" + str(DE))
    finally:
        print_table(("prof_name", "id"), "Profiles")


def add_profile_to_db(name):
    try:
        sql = "CREATE TABLE IF NOT EXISTS Profiles (prof_name VARCHAR(255), id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"
        sql_cursor.execute(sql)
        print("Table: Profiles created")
    except Exception as PE:
        print(PE)

    try:
        sql = "SELECT COUNT(1) FROM Profiles WHERE prof_name = \'" + str(name) + "\'"
        sql_cursor.execute(sql)
        if sql_cursor.fetchone()[0]:
            print("Name already exists")
        else:
            raise NonExistent
    except NonExistent:
        sql = "INSERT INTO Profiles (prof_name) VALUES(\'" + str(name) +"\')"
        print(sql)
        sql_cursor.execute(sql)
        database.commit()
    finally:
        print_table(("prof_name", "id"), "Profiles")


def add_file_to_db(file, path, profile):

    try:
        sql = "CREATE TABLE IF NOT EXISTS Files " \
              "(prof_name VARCHAR(255), " \
              "prof_key INT, " \
              "file_name VARCHAR(255), " \
              "file_path VARCHAR(255), " \
              "file_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"
        sql_cursor.execute(sql)
        print("Files table created or exists already, no error\n")
    except NonExistent:
        print("Could not create table Files")

    try:
        sql = "SELECT COUNT(1) FROM Profiles WHERE prof_name = \'" + str(profile) + "\'"
        sql_cursor.execute(sql)
        key = sql_cursor.fetchone()[0]

        sql = "INSERT INTO Files (prof_name, prof_key, file_path, file_name) VALUES(%s, %s, %s, %s)"
        val = (profile, key, path, file)
        sql_cursor.execute(sql, val)
        database.commit()
        print(sql_cursor.rowcount)
    except Exception as ADD_ERROR:
        print("Exception for adding file to database.\nError:\n" + str(ADD_ERROR))
    finally:
        print_table(("prof_name", "prof_key", "file_name", "file_path", "file_id"), "Files")


def delete_file_from_db(file, profile):
    try:
        sql = "SELECT COUNT(1) FROM Files WHERE file_name = \'" + str(file) + "\' AND prof_name = \'" + str(profile) + "\'"
        sql_cursor.execute(sql)
        if sql_cursor.fetchone()[0]:
            print("File can be deleted")
        else:
            raise NonExistent

    except NonExistent:
        print(str(file) + " could not been deleted.\n" + "Please check for typos\n")

    try:
        sql = "DELETE FROM Files WHERE file_name = \'" + str(file) + "\'"
        # sql = "DELETE FROM " + source + " WHERE " + label + " = " + "\'" + value + "\'"
        print("Your command for deleting: " + str(sql))
        sql_cursor.execute(sql)
        database.commit()
    except Exception as DEL_ERROR:
        print("Exception for deleting file from database.\nError:\n" + str(DEL_ERROR))
    finally:
        print_table(("prof_name", "prof_key", "file_name"), "Files")








