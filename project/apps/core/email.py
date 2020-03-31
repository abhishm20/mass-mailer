# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart

from settings import app_logger, RESOURCE_DIR


def get_config_data():
    """ To get json data from config."""
    with open(os.path.join(RESOURCE_DIR, 'config.json'), 'r') as fop:
        data = json.load(fop)
    return data


JSON_DATA = get_config_data()


class _SendEmailUsingSES:
    """
    This class used to send email using SES.
    """

    def __init__(self):
        self.JSON_DATA = JSON_DATA['ses']
        self.connection = self.get_server_connection()

    def get_server_connection(self):
        """
        To establish connection with SMTP server and return server connection.
        """
        server = smtplib.SMTP(self.JSON_DATA['SMTP_HOST'], self.JSON_DATA['SMTP_PORT'])
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.JSON_DATA['SMTP_USERNAME'], self.JSON_DATA['SMTP_PASSWORD'])
        return server

    def send_mail(self, msg_data):
        """ To Send email with attachments."""
        try:
            msg = MIMEMultipart('alternative')
            for key, value in msg_data['msg'].items():
                msg[key] = value
            msg.add_header('X-SES-CONFIGURATION-SET', 'ConfigSet')
            self.connection.sendmail(msg['From'], msg_data['rcpt'], msg.as_string())
            self.connection.close()
            # Display an error message if something goes wrong.
        except ConnectionError as e:
            app_logger.exception(e)
        except Exception as e:
            app_logger.exception(e)
        else:
            app_logger.log({
                'type': "EMAIL_SENT",
                'data': msg_data
            })


def send_email(email_data):
    data = json.loads(email_data)
    email_obj = _SendEmailUsingSES()
    email_obj.send_mail(data)
