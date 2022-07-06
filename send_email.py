import smtplib, sys
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
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

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
    year_month = str(year) + '-0' + str(month) if month<=9 else str(year) + '-' + str(month)
    # get last month and year, will send a request for file to be deleted
    month_p = month-1 if month != 1 else 12
    year_p = year if month != 1 else year-1
    year_month_prev = str(year_p) + '-0' + str(month_p) if month_p<=9 else str(year_p) + '-' + str(month_p)
    # create zip file
    zip_directory(year_month)
    # upload zip file to Dropbox
    upload_zip(year_month)
    # delete last month's zip if it exists
    try:
        delete_zip(year_month_prev)
    except:
        print(f"No zip file named {year_month_prev} found.")

    smtp_server = "smtp.gmail.com" 
    sender_email = "theautomatedemail@gmail.com"  #replace with airpartners email
    with open('app_password.txt', 'r') as f:
        password = f.read()

    send_mail(send_from=sender_email, send_to=['ndhulipala@olin.edu'], subject=f'Air Quality Reports {year_month}',
            message='These reports have been automatically generated based on last month\'s air quality data. '+
            'If you want to know more about how these visuals were made, please visit airpartners.org.\n\n\
            Please note that at the end of this month, the current zip file will be deleted and replaced\
            with this month\'s data.\n\n\
            https://www.dropbox.com/sh/spwnq0yqvjvewax/AADk0c2Tum-7p_1ul6xiKzrPa?dl=0 \n\n\
            Best regards,\nAir Partners',
            server=smtp_server, username=sender_email, password=password)