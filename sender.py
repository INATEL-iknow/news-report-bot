import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def _clean(s):
    """앞뒤 공백·줄바꿈 제거"""
    return (s or "").strip()

def send(subject, html, cfg):
    smtp_user = _clean(cfg.SMTP_USER)
    smtp_pass = _clean(cfg.SMTP_PASS)
    mail_from = _clean(cfg.MAIL_FROM)
    mail_to = [_clean(addr) for addr in cfg.MAIL_TO if _clean(addr)]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("뉴스 봇", mail_from))
    msg["To"] = ", ".join(mail_to)
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.sendmail(mail_from, mail_to, msg.as_string())
