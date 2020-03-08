# oh-my-email

## 什么是 oh-my-email

库如其名，`oh-my-email` 封装常用的邮件发送功能，使得在项目中发送邮件更加方便。

## 支持的功能

- [x] 简洁邮件发送API
- [x] 支持自定义发件人昵称
- [x] 支持抄送
- [x] 支持HTML
- [x] 支持附件

## 使用方式

安装 `oh-my-email`

```shell script
pip install oh-my-email
```

```python
from oh_my_email import (
    OhMyEmail, 
    OhMyEmailConfig, 
    OhMyEmailContact, 
    OhMyEmailPlainContent, 
    OhMyEmailHtmlContent
)
from oh_my_email.vo import UrlAttachment, FileAttachment

# 初始化配置
conf = OhMyEmailConfig(
    mail_host='',
    mail_port=25,
    mail_user='your email',
    mail_pass='your password',
)
ome = OhMyEmail(conf=conf)

# 发送纯文本邮件
with ome as cl:
    cl.send(
        subject='test subject',
        sender=OhMyEmailContact('sender email', 'sender name'),
        receiver=[OhMyEmailContact('receiver email', 'receiver name')],
        content=OhMyEmailPlainContent("This is a test email"),
    )

# 发送带抄送人和暗抄送人纯文本邮件
with ome as cl:
    cl.send(
        subject='test subject',
        sender=OhMyEmailContact('sender email', 'sender name'),
        cc=[OhMyEmailContact('cc email', 'cc name')],
        bcc=[OhMyEmailContact('bcc email', 'bcc name')],
        receiver=[OhMyEmailContact('receiver email', 'receiver name')],
        content=OhMyEmailPlainContent("This is a test email"),
    )


# 发送HTML邮件(会将html中包含的图片链接转为base64)
with ome as cl:
    img1 = "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2554525534.webp"
    text = f"""
    <p>Python 邮件发送测试...</p>
    <p>图片演示：</p>
    <p><img src="{img1}"></p>
    """
    cl.send(
        subject='test subject',
        sender=OhMyEmailContact('sender email', 'sender name'),
        receiver=[OhMyEmailContact('receiver email', 'receiver name')],
        content=OhMyEmailHtmlContent(text),
    )

# 发送带附件的邮件
with ome as cl:
    img1 = "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2554525534.webp"
    text = f"""
    <p>Python 邮件发送测试...</p>
    <p>图片演示：</p>
    <p><img src="{img1}"></p>
    """
    cl.send(
        subject='test subject',
        sender=OhMyEmailContact('sender email', 'sender name'),
        receiver=[OhMyEmailContact('receiver email', 'receiver name')],
        content=OhMyEmailHtmlContent(text),
        attachment=[UrlAttachment(url='', filename=''), FileAttachment(filepath='', filename='')]
    )
```