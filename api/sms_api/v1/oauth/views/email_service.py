from v1.oauth.views.gmail_smtp import GmailSMTPService

class EmailService:
	def create_email_service(provider_name, app):
		if provider_name == "gmail":
			return GmailSMTPService(app.config["GMAIL_SMTP_SETTINGS"])
		else:
			raise ValueError("Invalid email provider name")