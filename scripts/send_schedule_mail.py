"""Build today's idol schedule and email it via SMTP."""
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header

from scrape_schedule import build_body, today_jst


def send_mail(subject, body):
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    mail_from = os.environ.get("MAIL_FROM", user)
    mail_to = os.environ["MAIL_TO"]

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = mail_from
    msg["To"] = mail_to

    context = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
            server.login(user, password)
            server.sendmail(mail_from, [mail_to], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls(context=context)
            server.login(user, password)
            server.sendmail(mail_from, [mail_to], msg.as_string())


if __name__ == "__main__":
    today = today_jst()
    body = build_body(today)
    subject = f"【本日のスケジュール】{today.strftime('%Y/%m/%d')} 乃木坂46・櫻坂46・=LOVE"
    send_mail(subject, body)
    print("Sent.")
