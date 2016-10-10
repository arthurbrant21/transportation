import smtplib

class Mailer():

	def send_email(self, message, to_email):
		gmail_user = 'arthurbrant21.robot@gmail.com'
		gmail_pwd = '$teelers1'
		FROM = 'arthurbrant21.robot@gmail.com'
		TO = [to_email]
		SUBJECT = 'Daily Stock Report'
		TEXT = message

		# Prepare actual message
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.ehlo()
			server.starttls()
			server.login(gmail_user, gmail_pwd)
			server.sendmail(FROM, TO, message)
			server.close()
			print 'successfully sent the mail'
		except:
			print "failed to send mail"