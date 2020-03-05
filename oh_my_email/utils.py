# coding:utf-8
"""
description: 
author: jiangyx3915
date: 2020-03-05
"""
from typing import List
from oh_my_email.vo import OhMyEmailContact


def _serialize_contacts(contacts: List[OhMyEmailContact]) -> List[str]:
    return [item.render() for item in contacts]


def _serialize_contacts2str(contacts: List[OhMyEmailContact]) -> str:
    return ','.join(_serialize_contacts(contacts=contacts))