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
from oh_my_email.exception import ConnectHostException, EmailAuthException, SendMailException


@dataclass()
class OhMyEmailContact:
    email: str
    name: str = ""

    def render(self):
        return formataddr([self.name, self.email])


@dataclass()
class OhMyEmailConfig:
    mail_host: str
    mail_port: int
    mail_user: str
    mail_pass: str


class OhMyEmailBaseContent:

    def __init__(self, content, content_type, extra):
        self.content = content
        self.content_type = content_type
        self.extra = extra


class OhMyEmailPlainContent(OhMyEmailBaseContent):

    def __init__(self, content, extra=None):
        super().__init__(content, 'plain', extra)


class OhMyEmailHtmlContent(OhMyEmailBaseContent):
    def __init__(self, content, extra=None):
        super().__init__(content, 'html', extra)


def _serialize_contacts(contacts: List[OhMyEmailContact]) -> List[str]:
    return [item.render() for item in contacts]


def _serialize_contacts2str(contacts: List[OhMyEmailContact]) -> str:
    return ','.join(_serialize_contacts(contacts=contacts))


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
        return self

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
             sender: OhMyEmailContact,
             receiver: List[OhMyEmailContact],
             content: OhMyEmailBaseContent,
             cc: List[OhMyEmailContact] = None,
             bcc: List[OhMyEmailContact] = None,
             attachment=None) -> bool:
        """
        send email
        :param subject: email subject
        :param sender:      邮件发送人列表
        :param receiver:    邮件接收人列表
        :param cc:          抄送人列表
        :param bcc:         暗抄人列表
        :param content:
        :param attachment:
        :return:
        """
        real_from_email = sender.render()
        real_to_email = _serialize_contacts(receiver)

        message = MIMEText(content.content, content.content_type, 'utf-8')
        message.add_header('Subject', subject)
        message.add_header('From', real_from_email)
        message.add_header('To', ",".join(real_to_email))

        if cc:
            message.add_header('CC', _serialize_contacts2str(cc))

        if bcc:
            message.add_header('BCC', _serialize_contacts2str(bcc))

        try:
            self.smtp_client.sendmail(real_from_email, real_to_email, message.as_string())
        except Exception as e:
            raise SendMailException(f'Send Email Error，{str(e)}')
        return True
