### Start of new code section
## general information about each part
# notes about why/what certain lines of code do

#This is my main SQL functions and validation file
#I should really go over this more thoroughly but the same template that works has been used for
#every function in here so it might be OK
import sqlite3 as sql
from datetime import date
import re
##database shenanigans
today = date.today()
con = sql.connect("LabourersDB.db")

def databaseConnection(): #Connects to the SQL database
    try:
        con.row_factory = dictFactory #row_factory makes the connector return as a dictionary instead of a tuple, so I can edit it
        cursor = con.cursor()
        cursor.row_factory = dictFactory #Somehow I get a list of dictionaries from this, but it works so i dont question it
        return cursor
    except sqlite3.Error as error: #Will trigger if database not in same file, etc.
        print("Error while connecting to sqlite", error)

def dictFactory(cursor, row): #returns dictionary from a tuple
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary
## getting stuff out of the database
###Labourers
def getLabourersWithJob(job): #returns the IDs of all labourers with the job wanted, e.g. electrician, plumber, etc.
    try:
        command = "SELECT LabourerID FROM Labourers WHERE LabourerJob = ?" #I could use a switch statement here
        cursor.execute(command,str(job)) #to make the code more robust. Remember to do so at some stage.
        rows = cursor.fetchall()
        return rows[0]["LabourerIDs"]
    except:
        print("Invalid job. Please try again.")

def getLabourerWage(labourerID): #Gets the wage of a labourer to allow a payment to be calculated, or to show a customer before hire
    try: #try-except statement to catch exceptions, makes the program slightly more robust
        command = "SELECT LabourerWage FROM Labourers WHERE LabourerID = ?" #I cannot use a switch statement here
        cursor.execute(command,str(labourerID)) #as there are an infinite amount of possible inputs that are valid.
        rows = cursor.fetchall()
        return rows[0]["Labourer Wage"]
    except:
        print("Invalid ID. Please try again")

def getLabourerName(labourerID): #Gets the name of the labourer to be shown to the customer
    try:
        command = "SELECT LabourerName FROM Labourers WHERE LabourerID = ?"
        cursor.execute(command, str(labourerID))
        rows = cursor.fetchall()
        return rows[0]["Labourer Name"]
    except:
        print("Invalid ID. Please try again")

def getLabourerNumber(labourerID): #Returns the phone number of the labourer so he can be contacted either by the agency or the client
    command = """SELECT LabourerNumber FROM Labourers WHERE LabourerID = ?"""
    cursor.execute(command,str(labourerID))
    rows = cursor.fetchall()
    return rows[0]["LabourerNumber"]

def newLabourer(cursor): #Creates a new record for a newly hired worker
    try:
        name = input("Labourer name")
        year = int(input("Enter year born"))
        month = int(input("Enter month born (number)"))#by making them ints first I can validate w try/except    
        while month < 1 or month > 12: #Loops, forcing a valid number to be entered.
            month = int(input("Enter a valid month(number)"))
        day = int(input("Enter day born"))
        DOB = str(year)+"/"+str(month)+"/"+str(day) #I cannot connect them together without making them strs again
        number = int(input("Enter telephone number"))
        while len(str(number)) > 11: #Loops, forcing a valid number to be entered.
            number = int(input("Enter a valid number"))
        wage = float(input("Enter the worker's wage")) #always below minimum wage for maximum profit
        number = int(number)  #Further down the line I could use Regex to make sure these inputs adhere to a normal structure to avoid injections
        command = "SELECT max(LabourerID) FROM Labourers"
        cursor.execute(command)
        rows = cursor.fetchall()
        
        labourid = int(rows[0]["max(LabourerID)"]) + 1
        job = input("Enter job") #Will need to change this if I decide to limit the number of available jobs, maybe make a dropdown menu?
        command = """INSERT INTO Labourers(LabourerID,LabourerName,LabourerDOB,LabourerJob,LabourerWage, LabourerNumber)
        VALUES({},"{}","{}","{}",{},{})""".format(labourid, str(name),str(DOB),str(job),float(wage),int(number))
        cursor.execute(command) #Inserting parameters allows me to avoid SQL Injection attacks 
        con.commit()
    except:
        print("Something went wrong")


##Customers!!!!!
#Remember to use the HASHBYTES SQL function to encrypt passwords, using a salt to help protect against more attacks
def newCustomer(): #creates a new customer to extort for cash
    try: #Need to parameterise this at some point
        name = input("Enter your name")
        month = str(int(input("Enter the month you were born (number")))
        day = str(int(input("Enter the day you were born")))
        year = str(int(input("Enter the year you were born(4 digits)")))
        dob = day+month+year #I need to make a checkDate() function that tells me if something is a valid date
        while checkDate(dob) == False:
            month = input("Enter the month you were born (number") #I could edit my function to have it tell me what
            day = input("Enter the day you were born") #part is wrong but month and day are co-dependent
            year = input("Enter the year you were born (4 digits)") #so it could be either one, and year is co-dependent on february
            dob = day+"/"+month+"/"+year #Lucky I replace the slashes in the validation function as it saved a lot of time
        postcode = input("Enter postcode") #Use REGEX to check if this is in the proper form
        while isPostcode(postcode) == False:
            postcode = input("Enter postcode")
        housenumber = input("Enter number or house name") 
        road = input("Enter road name")
        address = housenumber + " " +road #There's no real rules on house numbers or roads, as sometimes they are
        #names for numbers and numbers for roads (e.g. if someone lives off the side of a dual carriageway for some reason)
        #for this reason I can't do as much validation without using something like Google Waypoints API or something
        password = input("Enter a password for the customer") #I should create a hashing algorithm and store the hashed password instead
        command = "SELECT max(CustomerID) FROM Customers"
        cursor.execute(command)
        rows = cursor.fetchall()
        customerid = rows[0]["max(CustomerID)"] + 1
        command = """INSERT INTO Customers(CustomerID,CustomerName,CustomerDOB,CustomerAddress,CustomerPostcode,CustomerPassword) VALUES(?,?,?,?,?,?""".format(int(customerid),str(name),str(dob),str(address),str(postcode),str(password))
        cursor.execute(command)
        con.commit()
    except:
        pass

def getCustomerAddress(customerid):
    try:
        command = """SELECT CustomerAddress FROM Customers WHERE CustomerID = ?"""
        cursor.execute(command,str(customerid))
        rows = cursor.fetchall()
        address = rows[0]["CustomerAddress"]
        return address
    except:
        pass

def getCustomerPostcode(customerid):
    try:
        command = """ SELECT CustomerPostcode FROM Customers WHERE CustomerID = ?"""
        cursor.execute(command,str(customerid))
        rows = cursor.fetchall()
        postcode = rows[0]["CustomerPostcode"]
        return postcode
    except:
        pass

def getCustomerName(customerid):
    try:
        command = """SELECT CustomerName FROM Customers WHERE CustomerID = ?"""
        cursor.execute(command,str(customerid))
        rows = cursor.fetchall()
        name = rows[0]["CustomerName"]
        return name
    except:
        pass

def getCustomerDOB(customerid):
    try:
        command = """SELECT CustomerDOB FROM Customers WHERE CustomerID = ?"""
        cursor.execute(command,str(customerid))
        rows = cursor.fetchall()
        dob = rows[0]["CustomerDOB"]
        return dob
    except:
        pass

###Orders

def newOrder():
    try:
        command = """SELECT max(OrderID) FROM Orders"""
        cursor.execute(command)
        rows = cursor.fetchall()
        orderid = rows[0]["OrderID"]+1
        command = """INSERT INTO Orders(OrderID,LabourerID,CustomerID,OrderStart,OrderEnd,PaymentID) VALUES(?,?,?,?,?,?) """.format(int(orderid),int(labourerid),int(customerid),str(orderstart),str(orderend),int(paymentid))
        cursor.execute(command)
        con.commit()
    except:
        pass

###Payments

def newPayment():
    try:
        command = """SELECT max(PaymentID) FROM Payments"""
        cursor.execute(command)
        rows = cursor.fetchall()
        paymentid = rows[0]["PaymentID"] + 1
        command = """INSERT INTO Payments(PaymentID,OrderID,AmountPaid,DatePaid) VALUES(?,?,?,?) """.format(int(paymentid),int(orderid),float(amountpaid),str(datepaid))
        cursor.execute(command)
        con.commit()
    except:
        pass


def isPostcode(postcode): #THIS WORKS NOW
    postcode.replace(" ","")  #Removes whitespace very nice to work with yes mhm
    postcode.upper()
    reg = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})" #I definitely wrote this myself mhm
    regRe = re.compile(reg) #Creates a regular expression object
    true = regRe.match(postcode) #If this does not match the pattern, returns None
    if true == None:
        return False
    else:
        return True

def checkDate(birthdate): #returns false if invalid, true if valid(Works exclusively with DD/MM/YYYY)
    try:
        birthdate = birthdate.replace("/","")#Removes slashes to make things super easy for me
        birthdate = birthdate.replace("-","") #Just in case I've somehow messed my database up that badly
        birthdate = birthdate.replace(".","") #Just. In. Case.
        if int(birthdate[2:4]) <=12:#I need to consider the varying number of days each month has
            if int(birthdate[2:4]) == 4 or int(birthdate[2:4]) == 6 or int(birthdate[2:4]) == 9 or int(birthdate[2:4]) == 11:
                if int(birthdate[2]) <= 30: #Switch statements would make the workload a lot easier here, but python :vomit:
                    return True
                else:
                    return False
            elif int(birthdate[2:4]) == 2:
                if int(birthdate[4:6]) % 4 == 0: #It may be more efficient to check the date first and only
                    if int(birthdate[2]) <= 29:#check if its a leap year when necessary instead of doing it every time
                        return True #I don't need to check if its false here since that will be verified at the next stage anyways
                elif int(birthdate[2]) <= 28:
                    return True
                else:
                    return False
    except:
        return False #since my code didn't work its clearly all the user's fault L
        

def passwordHash(password): #This gives a number which I can use to store my user's passwords. The only problem
    try: #is that two identical passwords will be stored the same way - I could try multiplying by user ID to remove
        total = 0 #this problem
        for i in range(len(password)):
            total = total + (int(ord(password[i])) * i) 
        print(total)
    except:
        pass
        

passwordHash(str(77))
    
