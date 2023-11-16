from v1.oauth.views.gmail_smtp import GmailSMTPService

class EmailService:
	def create_email_service(provider_name):
		if provider_name == "gmail":
			return GmailSMTPService()
		else:
			raise ValueError("Invalid email provider name")
