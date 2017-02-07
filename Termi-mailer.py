import email, getpass, imaplib, os, re 
print "Enter WebMail username"
prompt= ">"
user = raw_input(prompt)
print "Enter Password"
pwd = getpass.getpass( prompt)

# connecting to the webmail imap server
m = imaplib.IMAP4_SSL("newmailhost.cc.iitk.ac.in")
m.login(user,pwd)
m.select("INBOX")  # You can choose other mailboxes too  
resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items=items[0].split()



#Printing Top 10 Mails from Inbox
for emailid in range(1,50):
	
	resp, data = m.fetch(items[len(items)-emailid], "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, 
	email_body = data[0][1] # getting the mail content
	mail=email.message_from_string(email_body)
	#print type(mail)
	sender = mail['from'].split()[-1]
	#print mail['to']
	address = re.sub(r'[<>]','',sender)
	print emailid , mail['Subject']
	print address
	print "\n"
	#mail_num= raw_input("Enter the mail number:-")
mail_num=int(raw_input("Enter mail number"))
os.system("clear")		
resp, data = m.fetch(items[len(items)-mail_num], "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, 
email_body = data[0][1] # getting the mail content
#print email_body
mail=email.message_from_string(email_body)
#print mail
#print mail
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
	

for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename != "untitled-[2].html":
        	data = part.get_payload(decode=True)
        	if not data:
        		print 'No attachments...'
        		continue
        	f  = open( os.path.join( os.getcwd(),filename), 'w')
        	f.write(data)
        	f.close()



m.close()
m.logout()



        
