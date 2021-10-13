import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from typing import List

from secret_token import password


class SendEmailWithAttachment(Thread):
    email_host = 'smtp.qq.com'  # 服务器地址 163邮箱"smtp.163.com"  qq邮箱"smtp.qq.com"都需要开通smtp权限
    sender = 'cyjmmy@qq.com'  # 发件人（自己的邮箱）
    password = password

    def __init__(self, receivers: List[str], subject: str, txt: str, img: str, file: str = None):
        super().__init__()
        self.receivers = receivers
        self.subject = subject
        self.txt = txt
        self.file = file
        self.img = img

    def send_mail(self):
        # 多媒体邮件对象 可以带附件
        msg = MIMEMultipart()
        msg['Subject'] = self.subject  # 标题
        msg['From'] = ''  # 邮件中显示的发件人别称
        msg['To'] = ''  # ...收件人...

        msg.attach(MIMEText(self.txt, 'html', 'utf-8'))

        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        # 附件-图片
        if self.img is not None:
            if os.path.exists(self.img):
                with open(self.img, 'rb') as f:
                    image_content = f.read()
                image = MIMEImage(image_content, _subtype=subtype)
                img_name = os.path.basename(self.img)
                image.add_header('Content-Disposition', 'attachment', filename=img_name)
                msg.attach(image)
        # 附件-文件
        if self.file is not None:
            if os.path.exists(self.file):
                with open(self.file, 'rb') as f2:
                    file_content = f2.read()
                file = MIMEBase(maintype, subtype)
                file.set_payload(file_content)
                file_name = os.path.basename(self.file)
                file.add_header('Content-Disposition', 'attachment', filename=file_name)
                encoders.encode_base64(file)
                msg.attach(file)

        # 发送
        smtp = smtplib.SMTP()
        smtp.connect(self.email_host, 25)
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.receivers, msg.as_string())
        smtp.quit()
        print('邮件发送成功')

    def run(self):
        self.send_mail()


if __name__ == '__main__':
    SendEmailWithAttachment(['cyjmmy@foxmail.com'], '测试邮件01', '测试邮件内容', './1.jpg').start()
    print('正在发送邮件')
