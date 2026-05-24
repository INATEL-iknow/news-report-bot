import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send(subject, html, cfg):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("뉴스 봇", cfg.MAIL_FROM))
    msg["To"] = ", ".join(cfg.MAIL_TO)
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT) as s:
        s.starttls()
        s.login(cfg.SMTP_USER, cfg.SMTP_PASS)
        s.sendmail(cfg.MAIL_FROM, cfg.MAIL_TO, msg.as_string())