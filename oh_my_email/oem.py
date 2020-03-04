# coding:utf-8
"""
description:
author: jiangyx3915
date: 2020-03-04
"""
import smtplib
from typing import Union, List
from email.mime.text import MIMEText
from email.utils import formataddr
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


@dataclass()
class OhMyEmailContact:
    email: str
    name: str = ""


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
        self.smtp_client = None

    def get_client(self):
        if self.smtp_client is not None:
            return self.smtp_client
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
        return self.smtp_client

    def close_client(self):
        if self.smtp_client is None:
            return
        self.smtp_client.quit()
        self.smtp_client = None

    def __enter__(self):
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_client()

    def send(self, *,
             subject: str,
             from_email: str,
             to_email: List[OhMyEmailContact],
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
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = Header(self.conf.mail_sender, 'utf-8')
        to_email = [formataddr(item.name, item.email) for item in to_email]
        self.smtp_client.sendmail(from_email, to_email, message.as_string())
