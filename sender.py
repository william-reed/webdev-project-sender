import smtplib
import os


class PyMS:
    """
    Parent class to be utilized to send messages
    """

    def __init__(self,
                 username=None,
                 password=None,
                 host='smtp.gmail.com',
                 port=465):
        """
        :param username: account username. Defaults to 'PYMS_USERNAME' system environment variable
        :param password: account password. Defaults to 'PYMS_PASSWORD' system environment variable
        :param host: SMTP hostname
        :param port: SMTP port
        """
        self.username = username or os.environ.get('PYMS_USERNAME')
        self.password = password or os.environ.get('PYMS_PASSWORD')
        self.host = host
        self.port = port
        self.smtpserver = smtplib.SMTP_SSL(self.host, self.port)

    def connect(self):
        """
        Connect to the mail server
        :return self for chaining
        """
        self.smtpserver.ehlo()
        self.smtpserver.login(self.username, self.password)

    def disconnect(self):
        """
        Disconnect from SMTP server.
        :return: self for chaining
        """
        self.smtpserver.quit()

    def send_sms(self, phone_number, gateway, message):
        """
        Send an SMS
        :param phone_number: recipient phone number
        :param gateway: SMS gateway to use
        :param message: message body
        :return: self for chaining
        """
        self.smtpserver.sendmail(self.username, [phone_number + gateway], message)
