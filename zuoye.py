#!/usr/bin/env python
import sys
username = 'zzn'
password = '123456'
locked = 1
retry_counter = 0
while retry_counter < 3:
     user = raw_input('Username:').strip()
     if len(user) == 0:
         print '\033[31;1mUsername cannot be empty!\033[0m'
         #continue
         #break
     passwd = raw_input('Password:').strip()
     if len(passwd) == 0:
	     print '\033[031;1mPassword cannot be empty!\033[0m'
         #continue
         #break
 #handle the username and passwd empty issue
 #going to the loging verification part
 #means the user is locked
     if locked == 0:
         print 'Your username is locked!'
         sys.exit() 
     else:
         if user == username and passwd == password:
 #means passed the verfification
             sys.exit('Welcome %s login to our system!' % user)
         else:
             retry_counter += 1
             print '\033[31;1mWrong username or password,you have %s more chances!\033[0m' % (3 - retry_counter)
