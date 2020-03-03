# coding:utf-8
"""
description: 
author: jiangyx3915
date: 2020-03-03
"""
import smtplib
from typing import Union, List
from email.mime.text import MIMEText
from email.header import Header
from dataclasses import dataclass
from oh_my_email.exception import ConnectHostException, EmailAuthException


@dataclass()
class OhMyEmailConfig:
    mail_host: str
    mail_port: int
    mail_user: str
    mail_pass: str
    mail_sender: str


class OhMyEmailBaseContent:

    def __init__(self, content, content_type, extra):
        self.content = content
        self.content_type = content_type
        self.extra = extra


class OhMyEmailPlainContent(OhMyEmailBaseContent):

    def __init__(self, content, extra):
        super().__init__(content, 'plain', extra)


class OhMyEmailHtmlContent(OhMyEmailBaseContent):
    def __init__(self, content, extra):
        super().__init__(content, 'html', extra)


class OhMyEmail:

    def __init__(self, conf: OhMyEmailConfig):
        self.conf = conf
        self.smtp_client = smtplib.SMTP()
        try:
            self.smtp_client.connect(
                host=self.conf.mail_host,
                port=self.conf.mail_port)
        except Exception as e:
            raise ConnectHostException(f"Can not connect email server, {str(e)}")
        try:
            self.smtp_client.login(
                user=self.conf.mail_user,
                password=self.conf.mail_pass)
        except Exception as e:
            raise EmailAuthException(f"Auth Email SMTP Error, {str(e)}")

    def send(self, *,
             subject: str,
             from_email: str,
             to_email: Union[str, List[str]],
             content: OhMyEmailBaseContent,
             attachment):
        """
        send email
        :param subject: email subject
        :param from_email:
        :param to_email:
        :param content:
        :param attachment:
        :return:
        """
        message = MIMEText(content.content, content.content_type, 'utf-8')
        message['From'] = Header(self.conf.mail_sender, 'utf-8')
