from notify import Notifier
import logging
import smtplib
import sys

from email.mime.text import MIMEText


class EmailNotifier(Notifier):
    """ Notify owner using email
    """

    def __init__(self, client, email_info, owner):

        Notifier.__init__(self, client, email_info, owner)
        self.frm = email_info.get("from", None)
        self.name = email_info.get("name", None)
        self.smtp = email_info.get("smtp", None)
        self.username = email_info.get("username", None)
        self.password = email_info.get("password", None)


    def _do_notify(self, menace, instance, process, volume, applied_at, applied_duration):

        assert menace != None, "Menace not specified"
        assert instance != None, "Instance not specified"
        import pdb;pdb.set_trace()
        body = """ Details of Menace:
                        Client: %s
                        Applied At: %s
                        Applied Duration: %s
                        Menace Name: %s
                        Instance: %s
                        Process: %s
                        Volume: %s
                        Owner: %s
                        Owner Email: %s
                        Owner Phone: %s
                  """ % ( self.client,
                          applied_at,
                          applied_duration,
                          menace,
                          instance,
                          process if process else "NA",
                          volume if volume else "NA",
                          self.owner_name,
                          self.owner_email,
                          self.owner_phone if self.owner_phone else "NA")

        message = MIMEText(body, 'plain', 'utf-8')
        message["Subject"] = "Subject: Menace %s Created On %s" % ( menace, instance)
        message["From"] = self.frm
        message["To"] = self.owner_email
        s = smtplib.SMTP(self.smtp)
        s.starttls()
        s.login(self.username, self.password)
        s.sendmail(self.frm, [self.owner_email], message.as_string())
        s.quit()
