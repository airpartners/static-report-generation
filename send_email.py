"""
Author: Andrew DeCandia
Project: Air Partners

Script for sending emails with attachments from a gmail account.
"""
import smtplib
import sys
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from utils.zip_directory import zip_directory
from utils.dropbox_util import upload_zip
from utils.dropbox_util import delete_zip


def send_mail(send_from, send_to, subject, message, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """
    Compose and send email with provided info and attachments.

    :param send_from: (str) from name
    :param send_to: (list[str]) to name(s)
    :param subject (str): message title
    :param message (html): message body
    :param files (list[str]): list of file paths to be attached to email
    :param server (str): mail server host name
    :param port (int): port number
    :param username (str): server auth username
    :param password (str): server auth password
    :param use_tls (bool): use TLS mode
    :returns: none, sends an email
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    # get year and month from sys args
    year, month = int(sys.argv[1]), int(sys.argv[2])

    # Convert to date object
    date_obj = dt.date(year, month, 1)
    # format strings for current and previous month
    year_month = date_obj.isoformat()[:-3]
    year_month_prev = (date_obj - relativedelta(months=1)).isoformat()[:-3]

    # delete last month's zip if it exists
    try:
        delete_zip(year_month_prev)
    except:
        print(f"No zip file named {year_month_prev} found.")

    # create zip file
    zip_directory(year_month)
    # upload zip file to Dropbox; if file already exists, replace it
    try:
        upload_zip(year_month)
    except:
        delete_zip(year_month)
        upload_zip(year_month)

    # Get password from saved location
    with open('app_password.txt', 'r') as f:
        password = f.read()

    # Get list of subscribed emails to send to
    df = pd.read_csv('maillist.csv')
    df = df.loc[df['Status of Subscription'] == 'Subbed']
    mailing_list = df['Emails'].tolist()

    # Send emails individually to preserve anonymity of subscribers
    for email in mailing_list:
        send_mail(send_from='theautomatedemail@gmail.com',
              send_to=[email],
              subject=f'Air Quality Reports {year_month}',
              message="""
              <a href="https://www.dropbox.com/sh/spwnq0yqvjvewax/AADk0c2Tum-7p_1ul6xiKzrPa?dl=0">These reports</a> 
              have been automatically generated based on last month's air quality data. To access the reports, unzip 
              the folder and navigate to reports then pdfs. In graphs we have included high res images of the graphs 
              used in the reports for use in presentations or other media.<br>
              If you want to know more about how these visuals were made, please visit airpartners.org.<br><br>
              Please note that at the end of this month, the current zip file will be deleted and replaced with this 
              month's data.<br><br>
              Long Link:<br>https://www.dropbox.com/sh/spwnq0yqvjvewax/AADk0c2Tum-7p_1ul6xiKzrPa?dl=0<br><br>
              Best regards,<br>Air Partners<br><br><br>
              <a href="https://forms.gle/z9jPc8QNVRCCyChQ7">Unsubscribe</a>""",
              server='smtp.gmail.com', username='theautomatedemail@gmail.com', password=password)
