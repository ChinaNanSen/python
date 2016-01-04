#!/usr/bin/env python
#NameFile:test.py
#Import time module
import time
#Define a number of variables
sum = 0
#Registered account
user = input("User:").strip()
if len(user) == 0 :
    print ("User cannot be empty!!!")
elif len(user) > 6:
    print ("Your username is too long!!")
passwd = input("Passwd:")
if len(passwd) == 0 :
    print ("Passwd cannot be empty!!!")
elif len(passwd) > 6:
    print ("You set the password is too long!!")
#Format the user's account and password
list = """
     Your account password is as follows:
     user:%s
     passwd:%s"""%(user,passwd)
print (list)
print ("Congratulations on your registration,Please login again after five seconds.")
#Wait five seconds to allow the user to re-enter
time.sleep(5)
#Please login again
while sum < 3:
    User = input("please you input user:").strip()
    if len(User) == 0 :
        print ("User cannot be empty!!!")
    elif len(User) > 6:
        print ("Your username is too long!!")
    Passwd = input("please you input passwd:")
    if len(Passwd) == 0 :
        print ("paswd cannot be empty!!!")
    elif len(Passwd) > 6:
        print ("You set the password is too long!!")
    if User == user and Passwd == passwd:
        print ("Welcome you to log in.")
        break
    else:
        print ("Your account or password is incorrect. Please log in again.!!!")
#Number of users log on to count more than three times to lock the account
        sum += 1
        if sum > 4:
            print ("You log in too many, will lock your user!!!!")
