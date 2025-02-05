#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-10-21 20:00:14
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-13 22:33:44

import sys
import smtplib
import argparse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class SendMail:
    def __init__(self, recipients, content=None, attachments=None, config_file=None):
        self.recipients = recipients.split(',')
        self.content = content if content else "No content provided."
        self.attachments = attachments if attachments else []
        self.config_file = config_file if config_file else os.path.expanduser("~/.config/pysend.cfg")
        self.smtp_server, self.smtp_user, self.smtp_password = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                lines = f.read().strip().split()
                return lines[0], lines[1], lines[2]
        else:
            print(f"Warning: Configuration file {self.config_file} not found. Using default settings.")
            return "smtp.126.com", "wan230114@126.com", "cj1234567"

    def send(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Notification from SendMail'
        msg['From'] = self.smtp_user
        msg['To'] = ', '.join(self.recipients)

        # Attach the main content
        msg.attach(MIMEText(self.content, 'plain', 'utf-8'))

        # Attach files if any
        for attachment in self.attachments:
            if os.path.exists(attachment):
                with open(attachment, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                    msg.attach(part)
            else:
                print(f"Warning: Attachment {attachment} not found. Skipping.")

        try:
            with smtplib.SMTP(self.smtp_server, port=25, timeout=10) as smtp:
                smtp.login(self.smtp_user, self.smtp_password)
                smtp.sendmail(self.smtp_user, self.recipients, msg.as_string())
                print(f"Email sent successfully to {', '.join(self.recipients)}")
        except Exception as e:
            print(f"Failed to send email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send emails with text and attachments.")
    parser.add_argument("recipients", help="Recipient email addresses, separated by commas.")
    parser.add_argument("-c", "--content", help="Email content.", default=None)
    parser.add_argument("-f", "--attachments", nargs="+", help="List of files to attach.", default=None)
    parser.add_argument("--config", help="Path to configuration file (SMTP server, user, password).", default=None)

    args = parser.parse_args()

    mail_sender = SendMail(args.recipients, args.content, args.attachments, args.config)
    mail_sender.send()