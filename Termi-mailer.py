
##################################################################################
                                                                                 #
# Termi-mailer                                                                   #
# Python script to view mails and download attatchments from terminal            #
# Copyright- Saket Harsh IIT Kanpur                                              #
# E-Mail- sharsh2010@gmail.com                                                   #
##################################################################################



import email, getpass, imaplib, os, urllib2
prompt= ">"


def internet_on():
    try:
        response=urllib2.urlopen('https://www.google.co.in/',timeout=20)
        return True
    except urllib2.URLError as err: pass
    return False

if not internet_on():
	print "Internet not working ! Exiting"
	quit()


print "Enter WebMail username"
user = raw_input(prompt)
print "Enter Password"
pwd = getpass.getpass( prompt)

# Connecting to WebMail IMAP Server
m = imaplib.IMAP4_SSL("newmailhost.cc.iitk.ac.in")
m.login(user,pwd)
m.select("INBOX")      # You can choose other mailboxes too  . To know all existing mailboxes uncomment the line below
# print m.list
resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items=items[0].split()




#Printing Top 10 Mails from Inbox
for emailid in range(1,11):	
	resp, data = m.fetch(items[len(items)-emailid], "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, 
	email_body = data[0][1] # getting the mail content
	mail=email.message_from_string(email_body)
	sender = mail['from'].split()[-1]
	print sender
	print emailid , mail['Subject']
	print "\n"


# Taking User Input to show the Mail 
print "Enter Mail Number"	
mail_num=int(raw_input(prompt))
os.system("clear")   # Clear the screen to show fresh mail		
resp, data = m.fetch(items[len(items)-mail_num], "(RFC822)") 
email_body = data[0][1] 
mail=email.message_from_string(email_body)


# Two cases arise Either mail is multipart or text. Dealing both differently
if mail.is_multipart():
	bodytext=mail.get_payload()[0].get_payload();
	if type(bodytext) is list:
		bodytext=','.join(str(v) for v in bodytext)
	print "\n\n\n\n"
	print(' MESSAGE'.center(80, '*')), "\n"
	print "Subject:-" , mail['Subject']
	print "\n\n"
	print bodytext
else:
	print "\n\n\n\n"
	print(' MESSAGE '.center(80, '*')) , "\n"
	print "Subject:-" , mail['Subject']
	print "\n\n"
	print mail.get_payload()
	

# To download attachments if available
for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename != "untitled-[2].html":   # Default name of an untitled file that is never needed to be Downloaded 
        	print filename 
        	print "To Download press Y or y"
        	attach= raw_input(prompt)
        	if attach is "y" or "Y":
        		data = part.get_payload(decode=True)
        		if not data:
        			print 'No attachments...'
        			continue
        	
        	f  = open( os.path.join( os.getcwd(),filename), 'w')
        	f.write(data)
        	f.close()



m.close()
m.logout()





        
