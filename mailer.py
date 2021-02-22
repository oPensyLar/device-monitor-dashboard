import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from ssl import SSLError
from email import encoders
import socket
import os


class Mailer:
    serv_obj = None
    mime_obj = None
    usr = None
    msg = None
    srv = None
    prt = None
    verb = True

    def __init__(self):
        pass

    def set_srv(self, server, port):
        self.srv = server
        self.prt = port

    def set_body(self, recp, subject, attachment, body):
        email_sender = self.usr
        self.mime_obj = MIMEMultipart()
        self.mime_obj['From'] = email_sender
        self.mime_obj['To'] = recp
        self.mime_obj['Subject'] = subject

        if attachment is not None:
            filename = os.path.basename(attachment)
            attachment = open(attachment, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            self.mime_obj.attach(part)

        self.mime_obj.attach(MIMEText(body, 'plain'))

    def set_login(self, usr):
        self.usr = usr

    def conn(self):
        loop_flag = True

        while loop_flag:
            try:
                self.serv_obj = smtplib.SMTP(self.srv, self.prt)
                self.serv_obj.set_debuglevel(self.verb)
                # self.serv_obj.ehlo()
                # self.serv_obj.starttls()
                # self.serv_obj.login(self.usr, self.pwd)
                txt = self.mime_obj.as_string()
                self.serv_obj.sendmail(self.usr, self.mime_obj['To'], txt)
                self.serv_obj.quit()
                loop_flag = False

            except socket.gaierror:
                print("[!] socket.gaierror")

            except SSLError:
                print("[!] ssl.SSLError")

            except smtplib.SMTPConnectError:
                print("[!] SMTPServerDisconnected")

            except smtplib.SMTPServerDisconnected:
                print("[!] SMTPServerDisconnected")

        return
