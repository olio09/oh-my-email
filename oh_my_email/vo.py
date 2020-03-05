# coding:utf-8
"""
description: 
author: jiangyx3915
date: 2020-03-05
"""
import requests
from abc import abstractmethod
from dataclasses import dataclass
from email.utils import formataddr
from email.mime.application import MIMEApplication


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


class BaseAttachment:

    @abstractmethod
    def patch(self):
        raise NotImplemented()


class UrlAttachment(BaseAttachment):

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    def patch(self):
        raw = requests.get(self.url).content
        import ipdb
        part = MIMEApplication(raw)
        part.add_header('Content-Disposition', 'attachment', filename=self.filename)
        return part


class FileAttachment(BaseAttachment):

    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename

    def patch(self):
        with open(self.filepath, 'rb') as fp:
            part = MIMEApplication(fp.read())
            part.add_header('Content-Disposition', 'attachment', filename=self.filename)
            return part
