Hello,

This home assignment was part of my process to my previous position as a software developer at Safebreach .

The application:

Your setup should be able to receive emails from safebreach.com domain (Eg:israel@safebreach.com )
These emails will contain inside the body the keyword: “banana” and an attached python file 
Your application should be able to download the file, run it with python and send the output back to the recipient inside the email body

If keyword == ‘banana’, your application should send the output of the python attachment

If keyword != ‘banana’, your application should send an email with the following body: “Invalid keyword”

If the attachment is missing, your application should send an email with the following body: “Attachment missing”

If the python file you try to run throws an exception, your application should send an email with the backtrace of the exception
 

