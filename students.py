# @brief Creates a student database
# @file students.py
# @author Brandon Hughes
# @course CPSC-408-02 Database management
import random
import csv
import sqlite3

# create connection with database
conn = sqlite3.connect('./StudentDB')
mycursor = conn.cursor()


# makes sure strings contain only alpha characters or spaces
def contains_only_allowed_chars(input_string, allowedchars):
    for char in input_string:
        if char.isalpha() or char in allowedchars:
            continue
        else:
            return False
    return True


# imports file into database
def importdata(file):
    with open(file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            random_number = random.randint(1, 10)
            if random_number % 2 == 0:
                facadv = "Erik Linstead"
            else:
                facadv = "Elizabeth Stevens"
            mycursor.execute(
                "INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                + "ZipCode, MobilePhoneNumber, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['FirstName'], row['LastName'], row['GPA'], row['Major'], facadv, row['Address'], row['City'],
                 row['State'],
                 row['ZipCode'], row['MobilePhoneNumber'], 0))
    conn.commit()


# Display All Students and all of their attributes.
def allstudent():
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0")
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


# Add New Students
def addstudent(fn, ln, gpa, m, fa, add, c, s, zips, mobile):
    mycursor.execute(
        "INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (fn, ln, gpa, m, fa, add, c, s, zips, mobile, 0))
    conn.commit()


# Delete Students by StudentId
def deletestudent(inputstudentid):
    mycursor.execute(
        "UPDATE Student SET isDeleted = 1 WHERE StudentId = ?",
        (inputstudentid,))
    conn.commit()


# Update Students' major, advisor, or mobile phone number
def updatestudentmajor(inputstudentid, value):
    mycursor.execute(
        "UPDATE Student SET Major = ? WHERE StudentId = ?",
        (value, inputstudentid))
    conn.commit()


def updatestudentadvisor(inputstudentid, value):
    mycursor.execute(
        "UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?",
        (value, inputstudentid))
    conn.commit()


def updatestudentmobile(inputstudentid, value):
    mycursor.execute(
        "UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?",
        (value, inputstudentid))
    conn.commit()


# Search/Display students by Major, GPA, City, State and Advisor
def displaystudentmajor(value):
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND Major = ?",
                     (value,))
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


def displaystudentgpa(value):
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND GPA = ?",
                     (value,))
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


def displaystudentcity(value):
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND City = ?",
                     (value,))
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


def displaystudentstate(value):
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND State = ?",
                     (value,))
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


def displaystudentadv(value):
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, "
                     + "Zipcode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND FacultyAdvisor = ?",
                     (value,))
    rows = mycursor.fetchall()
    for row in rows:
        print(row)


# checks if a value is a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# import students
mycursor.execute("SELECT COUNT(*) FROM Student")
count = mycursor.fetchone()[0]

# check if students already has data that has been imported
if count == 0:
    importdata('/Users/student/downloads/students.csv')
    mycursor.execute("SELECT COUNT(*) FROM Student")
    count2 = mycursor.fetchone()[0]
    if count2 == 0:
        print("The table failed to import file.")
    else:
        print("The table imported the file.")
else:
    print("The table already imported data.")
allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
# main function of the program
while True:
    print("Please choose 1 of 6 options: (Input should be a num) ")
    print("1. Display All Students")
    print("2. Add a Student")
    print("3. Update a Student")
    print("4. Delete a Student")
    print("5. Search for a Student")
    print("6. Exit")
    user_input = input("Enter a Number: ")
    # checks what the user wants to do
    if user_input.isnumeric() and 6 >= int(user_input) >= 1:
        if int(user_input) == 1:
            allstudent()
            continue
        elif int(user_input) == 2:
            # create a new student
            # first name (must be alpha)
            while True:
                user_input = input("Enter the first name: ")
                if user_input.isalpha():
                    fname = user_input
                    break
                else:
                    print("Invalid first name. Only alpha characters are allowed.")
            # last name (must be alpha)
            while True:
                user_input = input("Enter the last name: ")
                if contains_only_allowed_chars(user_input, allowed_chars):
                    lname = user_input
                    break
                else:
                    print("Invalid last name. Only alpha characters are allowed.")
            # GPA (must be a x.x or x.xx)
            while True:
                user_input = input("Enter the GPA: ")
                if is_float(user_input) and 4.0 >= float(user_input) >= 0.1:
                    gpa = float(user_input)
                    gpa = round(gpa, 1)
                    break
                else:
                    print("Invalid GPA.")
            # Major (must be alpha)
            while True:
                user_input = input("Enter the major: ")
                if contains_only_allowed_chars(user_input, allowed_chars):
                    major = user_input
                    break
                else:
                    print("Invalid major. Please try again")
            # faculty advisor (must be 1 of 2 (Erik Linstead or Elizabeth Stevens))
            random_number = random.randint(1, 10)
            if random_number % 2 == 0:
                facadv = "Erik Linstead"
            else:
                facadv = "Elizabeth Stevens"
            # address (must be alpha)
            user_input = input("Enter the address: ")
            address = user_input
            # city (must be alpha)
            while True:
                user_input = input("Enter the city: ")
                if contains_only_allowed_chars(user_input, allowed_chars):
                    city = user_input
                    break
                else:
                    print("Invalid City. Please try again")
            # state (must be alpha)
            while True:
                user_input = input("Enter the state (full name of state): ")
                if contains_only_allowed_chars(user_input, allowed_chars):
                    state = user_input
                    break
                else:
                    print("Invalid state. Please try again")
            # zipcode (must be 5 digits)
            while True:
                user_input = input("Enter the zipcode (must be 5 digits): ")
                if user_input.isdigit() and len(user_input) == 5:
                    zipcode = user_input
                    break
                elif user_input.isdigit() and len(user_input) == 4:
                    zipcode = "0" + user_input
                    break
                elif user_input.isdigit() and len(user_input) == 3:
                    zipcode = "00" + user_input
                    break
                elif user_input.isdigit() and len(user_input) == 2:
                    zipcode = "000" + user_input
                    break;
                elif user_input.isdigit() and len(user_input) == 1:
                    zipcode = "0000" + user_input
                    break
                else:
                    print("Invalid zip code. Please try again")
            # mobilephonenumber (must be alpha)
            while True:
                user_input = input("Enter the phone number (No dashes inbetween ex. 1234567890): ")
                if user_input.isdigit():
                    mpn = user_input
                    break
                else:
                    print("Invalid phone number. Please try again")
            addstudent(fname, lname, gpa, major, facadv, address, city, state, zipcode, mpn)
            print("Added student to database")
            continue
        elif int(user_input) == 3:
            # update a student information
            while True:
                user_studentid = input("Enter the studentID of the information you want to update, or exit to quit ")
                # check's if the student exists
                mycursor.execute("SELECT * FROM Student WHERE studentid = ?", (user_studentid,))
                result = mycursor.fetchone()
                if result:
                    user_input = input("What would you like to update: "
                                       + "1. Major, 2. Advisor, 3. Mobile, or 4. Exit (please enter in words or 1,2,3) ")
                    if user_input.lower() == "major" or (user_input.isdigit() and int(user_input) == 1):
                        # change major
                        user_major = input("What is the new Major: ")
                        if contains_only_allowed_chars(user_major, allowed_chars):
                            updatestudentmajor(user_studentid, user_major)
                            print("Updated Major to " + user_major)
                            break
                        else:
                            print("Invalid Major")
                            continue
                    elif user_input.lower() == "advisor" or (user_input.isdigit() and int(user_input) == 2):
                        # change advisor
                        user_advisor = input("Who is the new advisor: ")
                        if contains_only_allowed_chars(user_advisor, allowed_chars):
                            updatestudentadvisor(user_studentid, user_advisor)
                            print("Updated Faculty Advisor to " + user_advisor)
                            break
                        else:
                            print("Invalid Advisor")
                            continue
                    elif user_input.lower() == "mobile" or (user_input.isdigit() and int(user_input) == 3):
                        # change mobile phone number
                        user_mobile = input("What is the new phone number (No dashes inbetween ex. 1234567890): ")
                        if user_mobile.isdigit():
                            updatestudentmobile(user_studentid, user_mobile)
                            print("Updated Phone Number to " + user_mobile)
                            break
                        else:
                            print("Invalid Phone Number")
                            continue
                    elif user_input == "Exit" or (user_input.isdigit() and int(user_input) == 4):
                        # exit
                        print("Exiting Updating Information for a Specific Student")
                        break
                    else:
                        continue
                elif user_studentid.lower() == "exit":
                    # exit
                    print("Exiting Updating Information")
                    break
                else:
                    # if student doesn't exist
                    print("StudentID does not exist in the database.")
                    continue
        elif int(user_input) == 4:
            # delete a user
            while True:
                user_studentid = input("Enter the studentID of the information you want to delete, or exit to quit ")
                # checks if any student exists
                mycursor.execute("SELECT * FROM Student WHERE studentid = ?", (user_studentid,))
                result = mycursor.fetchone()
                if result:
                    # set the isDeleted to 1
                    deletestudent(user_studentid)
                    break
                elif user_studentid.lower() == "exit":
                    print("Exiting Updating Information")
                    break
                else:
                    print("StudentID does not exist in the database.")
                    continue
            continue
        elif int(user_input) == 5:
            # search by a column
            user_column = input("Enter the information you would like to search by: "
                                + "1. Major, 2. GPA, 3. City, 4. State, 5. Advisor ")
            if user_column.isalpha() or 6 >= int(user_column) >= 1:
                print("Major should be complete name, GPA should be in x.x, City should have full name,"
                      + "State should have full name, and Advisor is both first and last name")
                user_value = input("What information should the search contain: "
                                   + "(Case Sensitive) ")
                if user_column.lower() == "major" or (user_column.isdigit() and int(user_column) == 1):
                    # searchs by major
                    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0 AND Major = ?",
                                     (user_value,))
                    result = mycursor.fetchone()
                    if result:
                        displaystudentmajor(user_value)
                    else:
                        print("Invalid Search")
                    continue
                elif user_column.lower() == "gpa" or (user_column.isdigit() and int(user_column) == 2):
                    # searchs by a certain gpa
                    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0 AND GPA = ?",
                                     (user_value,))
                    result = mycursor.fetchone()
                    if result:
                        displaystudentgpa(user_value)
                    else:
                        print("Invalid Search")
                    continue
                elif user_column.lower() == "city" or (user_column.isdigit() and int(user_column) == 3):
                    # searches by a city
                    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0 AND City = ?",
                                     (user_value,))
                    result = mycursor.fetchone()
                    if result:
                        displaystudentcity(user_value)
                    else:
                        print("Invalid Search")
                    continue
                elif user_column.lower() == "state" or (user_column.isdigit() and int(user_column) == 4):
                    # search by a state (full value)
                    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0 AND State = ?",
                                     (user_value,))
                    result = mycursor.fetchone()
                    if result:
                        displaystudentstate(user_value)
                    else:
                        print("Invalid Search")
                    continue
                elif user_column.lower() == "advisor" or (user_column.isdigit() and int(user_column) == 5):
                    # searches by the name of the advisors
                    mycursor.execute("SELECT * FROM Student WHERE IsDeleted = 0 AND FacultyAdvisor = ?",
                                     (user_value,))
                    result = mycursor.fetchone()
                    if result:
                        displaystudentadv(user_value)
                    else:
                        print("Invalid Search")
                    continue
                else:
                    print("Invalid Input.")
            else:
                print("Invalid Input.")
        elif int(user_input) == 6:
            # exit the whole program
            print("Exiting program")
            break
    else:
        # if the first 1-6 options aren't picked
        print("That is an unacceptable input. Please try again")
        continue

# close whole program
mycursor.close()
