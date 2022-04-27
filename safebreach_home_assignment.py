""""
This assignment was written by : Aviv Barel
"""

# libraries to import
import imaplib, email, smtplib, os
from subprocess import *

# server and user information variables
server_email = "safebreach@gmail.com"
server_password = "onetwo3456789"
server = 'imap.gmail.com'

"""
#An auxilary function which recives an email_message object
# and returns the body of the message as a string
"""

def get_body(email_message):
    if email_message.is_multipart():
        return get_body(email_message.get_payload(0))
    else:
        return email_message.get_payload(None, True)


"""
#An auxilary function which recives an email_message object
# and saves in the provided directory the attachment
# which is attached to the email
"""

def get_attachment(email_message, dir):
    filePath = None
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filePath = os.path.join(dir, filename)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))
    return filePath


""""
# The function recives the most recent email ,
# indicates if the keyword : "banana" is inside the body of the email
# extracts the attachment from the email, download it and saves it in the provided dir , 
# runs it ,saves the output, and sending it back to the sender in an email:
# if the keyword exist in the body and the python files runs successfully,
# it sends the output of the program of the python file
# if the keyword doesn't exist it sends an email back with the message : "missing keyword"
# if the keyword exist but the python file return an exception it sends an email back with
# the exception that was thrown
"""


def get_recent_email(dir):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(server_email, server_password)
    mail.select("Inbox")
    status, data = mail.search(None, "All")
    inbox_item_list = data[0].split()
    if len(inbox_item_list) == 0:
        print("No Emails")
        return
    most_recent = inbox_item_list[-1]
    res, email_data = mail.fetch(most_recent, '(RFC822)')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    address = email_message['From']
    body = str(get_body(email_message))
    if "banana" not in body:
        send_email(address, "Invalid keyword")
        return
    filePath = get_attachment(email_message, dir)
    if filePath == None:
        send_email(address, "Attachment missing")
        return
    else:
        command = ["python", filePath]
        try:
            output = check_output(command, stderr=STDOUT).decode()
        except CalledProcessError as e:
            output = e.output.decode()
        send_email(address, output)


""""
#An auxilary function that recives :
# String email address
# String message content
# sends the message content to the provided email address
"""


def send_email(address, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(server_email, server_password)
    message = f'Subject:  {"FeedBack"}\n\n{body}'
    server.sendmail(server_email, address, message)


def main():
    flag = input("Enter 1 to check the most recent email , Enter 0 to abort :  ")
    if flag =="1":
      dir = input(str("Enter the directory path to save the python file please : "))
      get_recent_email(dir)
      if(input("Would you like to check again ? 1- yes 0 - no  ")== "1"):
          main()
    else:
        quit()


main()
