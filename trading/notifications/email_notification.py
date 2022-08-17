from settings import EMAIL_PASSWORD
import smtplib


def send_email(subject: str, body: str, to_email: str = 'timschopinski@gmail.com'):
    gmail_user = 'timschopinski@gmail.com'
    gmail_password = EMAIL_PASSWORD
    sent_from = gmail_user
    to = [to_email]
    subject = subject
    body = body

    email_text = "Subject: {subject}\n\n{body}".format(subject=subject, body=body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)


if __name__ == '__main__':
    send_email('test', 'test')